import requests
import argparse

# === Configuration ===
API_URL = "https://projet-tiktok.onrender.com/run"  # <-- change cette URL

# === Argument parser ===
parser = argparse.ArgumentParser(description="Lancer un script distant via l'API Flask")
parser.add_argument("script", help="Nom du script à exécuter (ex: mon_script.py)")
parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments à transmettre au script")

args = parser.parse_args()

# === Corps de la requête ===
payload = {
    "script": args.script,
    "args": args.args
}

try:
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    print(f"✅ Réponse du serveur :\n{response.text}")
except requests.RequestException as e:
    print(f"❌ Erreur lors de la requête : {e}")