from flask import Flask, request, Response, stream_with_context
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Service actif. POST /run avec {'script': 'mon_script.py', 'args': ['...']}"

@app.route("/run", methods=["POST"])
def run_script():
    data = request.get_json()
    script = data.get("script")
    args = data.get("args", [])

    def generate():
        try:
            process = subprocess.Popen(
                ["python", script] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in iter(process.stdout.readline, ''):
                yield line

            process.stdout.close()
            process.wait()

        except Exception as e:
            yield f"❌ Erreur : {str(e)}"

    return Response(generate(), mimetype='text/plain')

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return "Aucun fichier reçu", 400

    save_path = os.path.join(".", file.filename)
    file.save(save_path)
    return f"✅ Fichier {file.filename} mis à jour avec succès"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)