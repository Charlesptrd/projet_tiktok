import os
import subprocess

def run(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Erreur : {result.stderr.strip()}")
    else:
        print(result.stdout.strip())

def main():
    print("📁 Mise à jour du dépôt GitHub")

    # Étape 1 : Ajouter tous les fichiers
    print("🔍 Étape 1 : git add .")
    run("git add .")

    # Étape 2 : Demander un message de commit
    message = input("✏️  Message de commit : ").strip()
    if not message:
        print("❌ Message vide. Abandon.")
        return

    # Étape 3 : Commit
    print(f"💾 Étape 2 : git commit -m \"{message}\"")
    run(f'git commit -m "{message}"')

    # Étape 4 : Push sur GitHub
    print("🚀 Étape 3 : git push origin main")
    run("git push origin main")

    print("✅ Terminé. Render va maintenant redéployer ton app.")

if __name__ == "__main__":
    main()