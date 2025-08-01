from flask import Flask, request
import subprocess
import os
import platform

app = Flask(__name__)

# Fonction pour sélectionner le bon exécutable selon l'OS
def get_executable_path(os_name="auto"):
    if os_name == "auto":
        os_name = platform.system().lower()

    mapping = {
        "mac": "./TwitchDownloaderCLI-macos",
        "linux": "./TwitchDownloaderCLI-linux",
        "win": "TwitchDownloaderCLI.exe"
    }

    return mapping.get(os_name, "./TwitchDownloaderCLI-linux")  # par défaut: linux

@app.route("/")
def home():
    return "✅ Service actif. POST /run avec {\"script\": \"nom.py\", \"os\": \"mac|linux|win\"}"

@app.route("/run", methods=["POST"])
def run_script():
    data = request.get_json()

    # Paramètres de la requête
    script = data.get("script")
    os_name = data.get("os", "auto").lower()

    if not script:
        return "❌ Aucun script spécifié.", 400

    # Exemple : si on veut exécuter un script Python
    if script.endswith(".py"):
        try:
            output = subprocess.check_output(["python", script], stderr=subprocess.STDOUT)
            return output.decode("utf-8")
        except subprocess.CalledProcessError as e:
            return f"❌ Erreur d'exécution Python :\n{e.output.decode()}", 500

    # Exemple : si on veut exécuter TwitchDownloaderCLI selon l'OS
    elif script == "twitch":
        exe_path = get_executable_path(os_name)
        try:
            os.chmod(exe_path, 0o755)  # Linux/mac seulement
            output = subprocess.check_output([exe_path, "--help"], stderr=subprocess.STDOUT)
            return output.decode("utf-8")
        except subprocess.CalledProcessError as e:
            return f"❌ Erreur d'exécution TwitchDownloaderCLI :\n{e.output.decode()}", 500
        except FileNotFoundError:
            return f"❌ Exécutable non trouvé pour l'OS : {os_name}", 404

    else:
        return f"❌ Script inconnu : {script}", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)