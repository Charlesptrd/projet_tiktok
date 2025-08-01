from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Service actif. POST /run avec {'script': 'nom.py'}"

@app.route("/run", methods=["POST"])
def run_script():
    data = request.get_json()
    script = data.get("script")

    # Vérification simple : on ne permet que certains scripts
    #allowed_scripts = ["script1.py", "script2.py"]
    #if script not in allowed_scripts:
        #return f"Script non autorisé : {script}", 400

    # Lancer le script (attention à la sécurité en prod !)
    try:
        output = subprocess.check_output(["python", script], stderr=subprocess.STDOUT)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'exécution :\n{e.output.decode()}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)