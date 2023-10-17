# -*- coding: utf-8 -*-
"""

Created on May 2022
@author: Mr ABBAS-TURKI

"""

from flask import Flask, render_template, redirect, url_for, request
import hashlib
import os

# définir le message secret
SECRET_MESSAGE = "alpine"
app = Flask(__name__)

RESOURCES_DIR = "resources/"
SERVER_PUBLIC_KEY_FILENAME = RESOURCES_DIR + "server-public-key.pem"
SERVER_PRIVATE_KEY_FILENAME = RESOURCES_DIR + "server-private-key.pem"

username = input("Veuillez entrer le nom d'utilisateur\n")
sel = os.urandom(8) # Création du sel (8 caractères)
hashpassword = hashlib.pbkdf2_hmac('sha256', bytes(input("Veuillez entrer le mot de passe pour l'utilisateur "+username+"\n") ,encoding="utf-8"), sel, 10) # Hash du mot de passe avec le sel et 10 itérations

@app.route("/", methods=["GET", "POST"])
def get_secret_message():
    
    error = None
    if request.method == "POST":
        hashEnteredPassword = hashlib.pbkdf2_hmac('sha256', bytes(request.form["password"],encoding="utf-8") , sel, 10) # Hash du mot de passe récupéré avec le sel et 10 itérations
        #request.form["password"] récupère le mot de passe entré dans le formulaire
        if request.form["username"] != username or hashEnteredPassword != hashpassword:
            error = "Nom d'utilisateur ou mot de passe incorect. Reessayez"
        else:
            return SECRET_MESSAGE
    return render_template("login.html", error=error)# on retourne la page web avec l'erreur si mot de passe incorrect


if __name__ == "__main__":
    # HTTPS version
    context = (SERVER_PUBLIC_KEY_FILENAME, SERVER_PRIVATE_KEY_FILENAME)
    app.run(debug=True, host="0.0.0.0", port=8081, ssl_context=context)
    # Route for handling the login page logic


   
