import requests
import argparse

# === Configuration ===
API_URL = "https://projet-tiktok.onrender.com/run"  # <-- change cette URL

# === Argument parser ===
parser = argparse.ArgumentParser(description="Lancer un script distant via l'API Flask")
parser.add_argument("script", help="Nom du script à exécuter (ex: test.py ou twitch)")
parser.add_argument("--os", default="auto", choices=["auto", "mac", "linux", "win"], help="Système d'exploitation ciblé (défaut: auto)")

args = parser.parse_args()

# === Corps de la requête ===
payload = {
    "script": args.script,
    "os": args.os
}

try:
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    print(f"✅ Réponse du serveur :\n{response.text}")
except requests.RequestException as e:
    print(f"❌ Erreur lors de la requête : {e}")