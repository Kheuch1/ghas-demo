import sqlite3
import subprocess
import os

# ================================================================
# DEMO GHAS - Code intentionnellement vulnérable
# NE JAMAIS utiliser ce code en production !
# ================================================================

# ---------------------------------------------------
# VULNÉRABILITÉ 1 : SQL Injection
# CodeQL détectera que 'username' vient de l'utilisateur
# et est inséré directement dans la requête SQL
# ---------------------------------------------------
def get_user_by_name(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # ❌ DANGEREUX : un attaquant peut écrire : ' OR '1'='1
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()

# ---------------------------------------------------
# VULNÉRABILITÉ 2 : Command Injection
# CodeQL détectera l'exécution d'une commande système
# construite avec une entrée utilisateur non filtrée
# ---------------------------------------------------
def list_user_files(user_input):
    # ❌ DANGEREUX : un attaquant peut écrire : "; rm -rf /"
    os.system("ls /home/" + user_input)

# ---------------------------------------------------
# VULNÉRABILITÉ 3 : Path Traversal
# Permet à un attaquant de lire n'importe quel fichier
# en tapant : ../../etc/passwd
# ---------------------------------------------------
def read_user_file(filename):
    # ❌ DANGEREUX : pas de validation du chemin
    with open("/var/data/" + filename, "r") as f:
        return f.read()

# ---------------------------------------------------
# Fonction principale (point d'entrée)
# ---------------------------------------------------
if __name__ == "__main__":
    user = input("Entrez un nom d'utilisateur : ")
    print(get_user_by_name(user))
