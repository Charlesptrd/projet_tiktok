import requests
import argparse

API_URL = "https://projet-tiktok.onrender.com/run"

parser = argparse.ArgumentParser()
parser.add_argument("script", help="Script à exécuter")
parser.add_argument("args", nargs=argparse.REMAINDER)
args = parser.parse_args()

payload = {
    "script": args.script,
    "args": args.args
}

import sys
import requests

SERVER_URL = "https://ton-app.onrender.com"  # remplace avec ton URL réelle

if sys.argv[1] == "upload":
    file_path = sys.argv[2]

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        try:
            r = requests.post(f"{SERVER_URL}/upload", files=files)
            r.raise_for_status()
            print(r.text)
        except requests.RequestException as e:
            print("❌ Erreur d'envoi :", e)
else:
    with requests.post(API_URL, json=payload, stream=True) as r:
        r.raise_for_status()
        print("📡 Réception de la sortie :\n")
        for line in r.iter_lines():
            if line:
                print(line.decode("utf-8"))