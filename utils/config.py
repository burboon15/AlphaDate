import os  
import json  
from cryptography.fernet import Fernet  

# Константы должны быть здесь!
CONFIG_FILE = "config.enc"  
KEY_FILE = "secret.key"  

class SecureConfig:  
    def __init__(self):  
        self.key = self._load_or_generate_key()  

    def _load_or_generate_key(self):  
        if os.path.exists(KEY_FILE):  
            with open(KEY_FILE, "rb") as f:  
                return f.read()  
        else:  
            key = Fernet.generate_key()  
            with open(KEY_FILE, "wb") as f:  
                f.write(key)  
            return key  

    def encrypt_data(self, data):  
        fernet = Fernet(self.key)  
        return fernet.encrypt(json.dumps(data).encode())  

    def decrypt_data(self, encrypted_data):  
        fernet = Fernet(self.key)  
        return json.loads(fernet.decrypt(encrypted_data).decode())  

    def save_credentials(self, username, password):  
        data = {"username": username, "password": password}  
        encrypted = self.encrypt_data(data)  
        with open(CONFIG_FILE, "wb") as f:  
            f.write(encrypted)  

    def load_credentials(self):  
        if not os.path.exists(CONFIG_FILE):  
            return None  
        
        with open(CONFIG_FILE, "rb") as f:  
            encrypted = f.read()  
            return self.decrypt_data(encrypted)  

    def clear_credentials(self):  
        if os.path.exists(CONFIG_FILE):  
            os.remove(CONFIG_FILE)  
        if os.path.exists(KEY_FILE):  
            os.remove(KEY_FILE)  