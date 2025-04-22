class User:
    def __init__(self, username, password, role="User"):
        self.username = username
        self.password = password  # In production, passwords should be hashed
        self.role = role

    def check_password(self, password):
        return self.password == password

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

    @staticmethod
    def from_dict(data):
        return User(data["username"], data["password"], data.get("role", "User"))

    def __repr__(self):
        return f"User(username={self.username}, role={self.role})"
