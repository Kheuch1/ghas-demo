import sqlite3
import os

# ================================================================
# DEMO GHAS - Code intentionnellement vulnérable
# NE JAMAIS utiliser ce code en production !
# ================================================================

# VULNÉRABILITÉ 1 : SQL Injection
def get_user_by_name(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()

# VULNÉRABILITÉ 2 : Command Injection
def list_user_files(user_input):
    os.system("ls /home/" + user_input)

# VULNÉRABILITÉ 3 : Path Traversal
def read_user_file(filename):
    with open("/var/data/" + filename, "r") as f:
        return f.read()

if __name__ == "__main__":
    user = input("Entrez un nom d'utilisateur : ")
    print(get_user_by_name(user))
