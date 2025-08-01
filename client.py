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

with requests.post(API_URL, json=payload, stream=True) as r:
    r.raise_for_status()
    print("📡 Réception de la sortie :\n")
    for line in r.iter_lines():
        if line:
            print(line.decode("utf-8"))