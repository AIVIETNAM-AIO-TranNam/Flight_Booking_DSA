import csv
from src.models import HashTable

class UserManagerModule:
    def __init__(self, filepath="data/users.csv"):
        self.users_table = HashTable()
        self.current_user = None
        self.filepath = filepath

    def load_users_from_file(self, filepath=None):
        target_path = filepath or self.filepath 
        #if filepath provided: target_path = filepath
        #else: target_path = self.filepath
        try:
            with open(target_path, "r", encoding="utf-8", newline = "") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    if row == ["username", "password", "role"]:
                        continue
                    if len(row) == 3:
                        username, password, role = row
                        self.users_table.insert(
                            username,
                            {"password": password, "role": role}
                        )
        except FileNotFoundError:
            pass

    def register_user(self, username, password, role="customer"):
        if self.users_table.get(username):
            return False, "Username already exists!"
        self.users_table.insert(username, {"password": password, "role": role})
        with open(self.filepath, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, role])
        return True, "Registration successful!"

    def authenticate_user(self, username, password):
        user_data = self.users_table.get(username)
        if user_data and user_data["password"] == password:
            self.current_user = {"username": username, "role": user_data["role"]}
            return True, "Login successful!"
        return False, "Invalid username or password!"