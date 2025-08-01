import requests

# 🔧 Change cette URL par celle de ton app déployée (Render, Railway, etc.)
SERVER_URL = "https://ton-app.onrender.com/run"

def run_remote_script(script_name):
    payload = {"script": script_name}
    try:
        response = requests.post(SERVER_URL, json=payload)
        if response.status_code == 200:
            print(f"✔️ Résultat du script '{script_name}':\n")
            print(response.text)
        else:
            print(f"❌ Erreur {response.status_code} : {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion : {e}")

if __name__ == "__main__":
    print("Liste des scripts disponibles : script1.py, script2.py")
    script = input("Quel script veux-tu lancer ? ")
    run_remote_script(script)