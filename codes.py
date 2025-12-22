# ---------- Python ----------
import os
import yaml

# Command Injection
os.system("cat " + user_input)

# SQL Injection
query = "SELECT * FROM users WHERE id=" + user_id
cursor.execute(query)

# Unsafe YAML Load
config = yaml.load(open("config.yml"), Loader=yaml.Loader)

# Hardcoded Password
DB_PASSWORD = "admin123"
