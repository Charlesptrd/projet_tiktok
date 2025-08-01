from flask import Flask, request, Response, stream_with_context
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Service actif. POST /run avec {'script': 'mon_script.py', 'args': ['...']}"

@app.route("/run", methods=["POST"])
def run_script():
    data = request.get_json()
    script = data.get("script")
    args = data.get("args", [])
    
    if not script:
        return "❌ Aucun script spécifié.", 400

    command = ["python", script] + args
    print(f"▶️ Commande : {' '.join(command)}")

    def generate():
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        for line in iter(process.stdout.readline, ''):
            yield line

        process.stdout.close()
        process.wait()

    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)