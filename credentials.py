import csv

class CredentialManager:
    def __init__(self, credential_file):
        self.users = self.read_credentials(credential_file)

    def read_credentials(self, file_path):
        users = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(row['username'], row['password'], row['role'])
                users.append(user)
        return users

    def validate_user(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
