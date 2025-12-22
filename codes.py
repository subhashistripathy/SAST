import os
import subprocess
import sqlite3
import pickle
import yaml
import requests
import hashlib
import hmac
import smtplib
from flask import Flask, request

app = Flask(__name__)

# ------------------------------
# 1. OS Command Injection
# ------------------------------
def list_dir():
    folder = input("Enter folder: ")
    os.system("ls " + folder)  # ❌ command injection

# ------------------------------
# 2. Subprocess Injection
# ------------------------------
def run_ping():
    ip = input("Enter IP: ")
    subprocess.call("ping " + ip, shell=True)  # ❌

# ------------------------------
# 3. SQL Injection
# ------------------------------
def get_user(uid):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=" + uid)  # ❌ SQL Injection
    return cursor.fetchall()

# ------------------------------
# 4. Insecure Deserialization
# ------------------------------
def load_user(data):
    obj = pickle.loads(data)  # ❌ arbitrary code execution
    return obj

# ------------------------------
# 5. Unsafe YAML Load
# ------------------------------
def load_yaml(content):
    config = yaml.load(content, Loader=yaml.Loader)  # ❌ unsafe YAML
    return config

# ------------------------------
# 6. Hardcoded Secrets
# ------------------------------
API_KEY = "1234567890abcdef"  # ❌

# ------------------------------
# 7. Weak Cryptography / MD5
# ------------------------------
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # ❌ weak hash

# ------------------------------
# 8. Hardcoded HMAC Key
# ------------------------------
HMAC_KEY = "supersecretkey123"  # ❌

# ------------------------------
# 9. HTTP Request without TLS verification
# ------------------------------
def insecure_request(url):
    return requests.get(url, verify=False).text  # ❌ disables cert verification

# ------------------------------
# 10. Email Sending with Hardcoded Credentials
# ------------------------------
def send_email():
    server = smtplib.SMTP("smtp.example.com")
    server.login("user@example.com", "password123")  # ❌ hardcoded credentials
    server.sendmail("from@example.com", "to@example.com", "Hello!")

# 11. Flask Debug Mode Enabled
if __name__ == "__main__":
    app.run(debug=True)  # ❌ debug mode exposes info
