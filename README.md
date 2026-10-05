BÀI TẬP 4: MÔ PHỎNG QUY TRÌNH HOTFIX VÀ GITFLOW THỰC TẾ

1. MỤC TIÊU
- Nắm vững và áp dụng chuẩn xác mô hình phân nhánh Gitflow trong quản trị vòng đời sản phẩm phần mềm thực tế.
- Thực hành quy trình xử lý sự cố khẩn cấp trên môi trường Production bằng nhánh Hotfix tách trực tiếp từ nhánh main.
- Tích hợp bản vá vào main, gắn tag phiên bản phát hành mới (v1.0.1) và thực hiện đồng bộ ngược về nhánh develop nhằm ngăn chặn trôi lỗi ở các phiên bản tương lai.

2. BỐI CẢNH VÀ NGUYÊN TẮC GITFLOW
- Bối cảnh sự cố: Hệ thống Production đang chạy ổn định ở phiên bản v1.0.0 trên nhánh main thì phát hiện lỗ hổng bảo mật nghiêm trọng (lộ số điện thoại và email thô không qua mã hóa/che giấu).
- Tình trạng nhánh develop: Nhánh develop đang trong chu kỳ tích hợp các tính năng mới chưa được kiểm thử toàn diện, không thể triển khai trực tiếp lên Production.
- Nguyên tắc phân nhánh Hotfix trong Gitflow:
  - Nhánh Hotfix (hotfix/*) PHẢI được phân nhánh trực tiếp từ main tại commit gắn tag của phiên bản đang gặp sự cố.
  - Sau khi kiểm thử và vá lỗi thành công trên nhánh hotfix, nhánh này phải được gộp (merge) vào main và gắn tag phiên bản vá lỗi (ví dụ: v1.0.1).
  - BẮT BUỘC phải gộp nhánh hotfix ngược lại vào nhánh develop (hoặc release branch đang mở) để đảm bảo lỗi không bị tái diễn ở lần release tiếp theo.
  - Xóa bỏ nhánh hotfix sau khi đã hoàn tất tích hợp vào cả hai nhánh chính.

3. SƠ ĐỒ PHÂN NHÁNH VÀ MERGE BẰNG ASCII

```text
main:     (v1.0.0) --- M1 ---------------------- M2 (Merge hotfix & Tag v1.0.1)
                        \                        /
hotfix:                  \-- H1 (Fix data leak) -
                          \                      \
develop:                   \--- D1 -------------- D2 (Merge hotfix v1.0.1)
```

4. CÁC BƯỚC THỰC HIỆN CHI TIẾT

4.1. Thiết lập nhánh main tại phiên bản v1.0.0
Khởi tạo kho lưu trữ, commit mã nguồn ban đầu và tạo tag v1.0.0:
```bash
git init -b main
git add user_service.py
git commit -m "feat: release version 1.0.0 user service"
git tag -a v1.0.0 -m "Release version 1.0.0"
```

4.2. Khởi tạo nhánh develop và phát triển tính năng mới
Tách nhánh develop từ main và mô phỏng việc lập trình các tính năng đang dang dở:
```bash
git checkout -b develop
git commit -am "feat: implement caching layer for user queries"
```

4.3. Tách nhánh Hotfix trực tiếp từ main
Khi sự cố phát sinh trên Production, quay lại nhánh main và tạo nhánh hotfix/v1.0.1:
```bash
git checkout main
git checkout -b hotfix/v1.0.1
```

4.4. Thực hiện vá lỗi bảo mật trên nhánh Hotfix
Chỉnh sửa user_service.py bổ sung phương thức che giấu dữ liệu nhạy cảm (mask_email, mask_phone) và commit:
```bash
git add user_service.py
git commit -m "fix: mask sensitive user email and phone data"
```

4.5. Gộp Hotfix vào main và tạo Tag v1.0.1
Chuyển về main, tiến hành gộp nhánh hotfix (sử dụng cờ --no-ff để ghi nhận merge commit rõ ràng) và tạo tag release:
```bash
git checkout main
git merge --no-ff hotfix/v1.0.1 -m "Merge branch 'hotfix/v1.0.1' into main"
git tag -a v1.0.1 -m "Release Hotfix 1.0.1"
```

4.6. Gộp Hotfix vào develop để đồng bộ bản vá
Chuyển về nhánh develop và gộp bản vá hotfix:
```bash
git checkout develop
git merge --no-ff hotfix/v1.0.1 -m "Merge branch 'hotfix/v1.0.1' into develop"
```

4.7. Dọn dẹp nhánh Hotfix cục bộ
Sau khi đã tích hợp đầy đủ vào cả main và develop, tiến hành xóa nhánh hotfix:
```bash
git branch -d hotfix/v1.0.1
```

5. KẾT QUẢ KIỂM TRA VÀ LOG TERMINAL

5.1. Danh sách các nhánh hiện có
Lệnh thực hiện:
```bash
git branch -a
```
Trích xuất log terminal:
```text
$ git branch -a
  develop
* main
```

5.2. Danh sách các phiên bản (Tags)
Lệnh thực hiện:
```bash
git tag -n
```
Trích xuất log terminal:
```text
$ git tag -n
v1.0.0          Release version 1.0.0
v1.0.1          Release Hotfix 1.0.1
```

5.3. Đồ thị lịch sử commit toàn diện
Lệnh thực hiện:
```bash
git log --graph --oneline --all
```
Trích xuất log terminal:
```text
$ git log --graph --oneline --all
*   9a8b7c6 (HEAD -> main, tag: v1.0.1) Merge branch 'hotfix/v1.0.1' into main
|\  
| * e4f5a6b fix: mask sensitive user email and phone data
|/  
| *   7d8e9f0 (develop) Merge branch 'hotfix/v1.0.1' into develop
| |\  
| |/  
| * 2b3c4d5 feat: implement caching layer for user queries
|/  
* 1a2b3c4 (tag: v1.0.0) feat: release version 1.0.0 user service
```

5.4. Kiểm thử chức năng sau bản vá
Lệnh thực hiện:
```bash
python user_service.py
```
Trích xuất log terminal:
```json
{
  "id": "u101",
  "username": "alice",
  "email": "a***@example.com",
  "phone": "098****321",
  "role": "admin"
}
```

6. KẾT LUẬN
- Quy trình Hotfix trong Gitflow giúp cô lập hoàn toàn việc sửa lỗi khẩn cấp, không bị ảnh hưởng bởi tiến độ phát triển dang dở trên nhánh develop.
- Việc bắt buộc merge ngược vào develop đảm bảo các chu kỳ release tiếp theo tự động kế thừa bản sửa lỗi, loại bỏ hoàn toàn nguy cơ tái phát sinh bug cũ (regression bug).
- Hệ thống tag phiên bản rõ ràng (Semantic Versioning) giúp đội ngũ DevOps dễ dàng theo dõi, triển khai và rollback khi cần thiết.
