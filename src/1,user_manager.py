from src.models import HashTable

class UserManagerModule:
    def __init__(self):
        self.users_table = HashTable()
        self.current_user = None

    def load_users_from_file(self, filepath="data/users.txt"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        username, password, role = parts
                        self.users_table.insert(username, {"password": password, "role": role})
        except FileNotFoundError:
            pass

    def register_user(self, username, password, role="customer"):
        if self.users_table.get(username):
            return False, "Username already exists!"
        self.users_table.insert(username, {"password": password, "role": role})
        with open("data/users.txt", "a", encoding="utf-8") as f:
            f.write(f"{username},{password},{role}\n")
        return True, "Registration successful!"

    def authenticate_user(self, username, password):
        user_data = self.users_table.get(username)
        if user_data and user_data["password"] == password:
            self.current_user = {"username": username, "role": user_data["role"]}
            return True, "Login successful!"
        return False, "Invalid username or password!"