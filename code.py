# ==============================
# VULNERABLE PYTHON CODE (LAB)
# ==============================

import os
import pickle
import yaml
import subprocess
import sqlite3
import hashlib
import tempfile
import ssl
import requests
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# ------------------------------
# 1. OS Command Injection
# ------------------------------
@app.route("/ping")
def ping():
    host = request.args.get("host")
    os.system("ping " + host)   # ❌ command injection
    return "OK"


# ------------------------------
# 2. Subprocess Injection
# ------------------------------
@app.route("/nslookup")
def nslookup():
    domain = request.args.get("domain")
    subprocess.call("nslookup " + domain, shell=True)  # ❌
    return "Done"


# ------------------------------
# 3. SQL Injection
# ------------------------------
@app.route("/user")
def get_user():
    uid = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=" + uid)  # ❌
    return str(cursor.fetchall())


# ------------------------------
# 4. Insecure Deserialization
# ------------------------------
@app.route("/load")
def load_object():
    data = request.args.get("data").encode()
    obj = pickle.loads(data)  # ❌ arbitrary code execution
    return str(obj)


# ------------------------------
# 5. Unsafe YAML Load
# ------------------------------
@app.route("/config")
def load_config():
    content = request.args.get("yml")
    config = yaml.load(content, Loader=yaml.Loader)  # ❌
    return str(config)


# ------------------------------
# 6. Hardcoded Secret
# ------------------------------
SECRET_KEY = "super_secret_key_123456"  # ❌


# ------------------------------
# 7. Weak Hashing Algorithm
# ------------------------------
def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()  # ❌ weak crypto


# ------------------------------
# 8. SSRF (Server-Side Request Forgery)
# ------------------------------
@app.route("/fetch")
def fetch_url():
    url = request.args.get("url")
    return requests.get(url).text  # ❌ SSRF


# ------------------------------
# 9. Open Redirect
# ------------------------------
@app.route("/redirect")
def open_redirect():
    url = request.args.get("next")
    return redirect(url)  # ❌ open redirect


# ------------------------------
# 10. XSS (Server-side template injection)
# ------------------------------
@app.route("/hello")
def hello():
    name = request.args.get("name")
    return render_template_string("<h1>Hello %s</h1>" % name)  # ❌ XSS


# ------------------------------
# 11. Insecure Temporary File
# ------------------------------
def temp_file():
    f = tempfile.mktemp()  # ❌ race condition
    open(f, "w").write("data")


# ------------------------------
# 12. TLS Certificate Verification Disabled
# ------------------------------
def insecure_request():
    requests.get("https://example.com", verify=False)  # ❌


# ------------------------------
# 13. Weak SSL Configuration
# ------------------------------
context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)  # ❌ deprecated protocol


# ------------------------------
# 14. Path Traversal
# ------------------------------
@app.route("/read")
def read_file():
    filename = request.args.get("file")
    with open("/data/" + filename) as f:  # ❌ path traversal
        return f.read()


# ------------------------------
# 15. Debug Mode Enabled
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)  # ❌ information disclosure
