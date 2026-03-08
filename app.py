import sqlite3
import os
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)

# ================================================================
# DEMO GHAS - Code intentionnellement vulnérable
# NE JAMAIS utiliser ce code en production !
# ================================================================

# VULNÉRABILITÉ 1 : SQL Injection
# Source : request.args.get("username") = entrée HTTP
# Sink   : cursor.execute(query) = exécution SQL
@app.route("/user")
def get_user():
    username = request.args.get("username")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return str(cursor.fetchall())

# VULNÉRABILITÉ 2 : Command Injection
# Source : request.args.get("folder") = entrée HTTP
# Sink   : subprocess.run() = exécution système
@app.route("/files")
def list_files():
    folder = request.args.get("folder")
    result = subprocess.run(
        "ls /home/" + folder,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout

# VULNÉRABILITÉ 3 : Path Traversal
# Source : request.args.get("filename") = entrée HTTP
# Sink   : send_file() = lecture de fichier
@app.route("/download")
def download_file():
    filename = request.args.get("filename")
    return send_file("/var/data/" + filename)

if __name__ == "__main__":
    app.run(debug=True)
```

### 3. Committez les deux fichiers → attendez 3-5 min → retournez dans **Security → Code scanning**

---

## ⏱️ Ce que CodeQL va maintenant tracer
```
/user?username=...
      ↓
   username = request.args.get("username")   ← SOURCE détectée
      ↓
   query = "SELECT..." + username             ← propagation
      ↓
   cursor.execute(query)                      ← SINK ⚠️ ALERTE !
