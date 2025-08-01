from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Service actif. POST /run avec {'script': 'nom.py', 'args': ['arg1', 'arg2']}"

@app.route("/run", methods=["POST"])
def run_script():
    data = request.get_json()
    script = data.get("script")
    args = data.get("args", [])

    if not script:
        return "❌ Aucun script spécifié.", 400

    command = ["python", script] + args
    print(f"🔧 Exécution de : {' '.join(command)}")

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"❌ Erreur d'exécution :\n{e.output.decode()}", 500
    except FileNotFoundError:
        return f"❌ Fichier script introuvable : {script}", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)