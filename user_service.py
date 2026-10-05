import json

class UserService:
    def __init__(self):
        self.users = {
            "u101": {
                "id": "u101",
                "username": "alice",
                "email": "alice@example.com",
                "phone": "0987654321",
                "ssn": "123-45-6789",
                "role": "admin"
            },
            "u102": {
                "id": "u102",
                "username": "bob",
                "email": "bob@example.com",
                "phone": "0912345678",
                "ssn": "987-65-4321",
                "role": "user"
            }
        }

    def get_user_profile(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return None
        return {
            "id": user["id"],
            "username": user["username"],
            "email": self._mask_email(user["email"]),
            "phone": self._mask_phone(user["phone"]),
            "role": user["role"]
        }

    def _mask_email(self, email):
        parts = email.split("@")
        if len(parts) != 2:
            return "***"
        name, domain = parts
        masked_name = name[0] + "***" if len(name) > 1 else "***"
        return f"{masked_name}@{domain}"

    def _mask_phone(self, phone):
        if len(phone) < 4:
            return "***"
        return phone[:3] + "****" + phone[-3:]

if __name__ == "__main__":
    service = UserService()
    profile = service.get_user_profile("u101")
    print(json.dumps(profile, indent=2))
