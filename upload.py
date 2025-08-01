import os
import shutil
from datetime import datetime
import time

def secondes_jusqua(annee, mois, jour, heure=0, minute=0, seconde=0):
    """
    Renvoie le nombre de secondes entre maintenant et une date/heure future.
    Si la date est dans le passé, retourne 0.
    
    :return: float - secondes restantes
    """
    date_cible = datetime(annee, mois, jour, heure, minute, seconde)
    maintenant = datetime.now()
    delta = date_cible - maintenant

    return max(0, delta.seconds)


def remplacer_video(nouvelle_video_path, dossier_cible):

    nom_fichier = os.path.basename(nouvelle_video_path)
    chemin_cible = os.path.join(dossier_cible, nom_fichier)

    if os.path.exists(chemin_cible):
        os.remove(chemin_cible)

    shutil.copy(nouvelle_video_path, chemin_cible)  # Pas de métadonnées copiées


def upload_on_tiktok(video_path, tiktok_username, title="Ceci est un titre oublié #fyp", date=0):
    remplacer_video(video_path, "/Users/charles/Desktop/test/TiktokAutoUploader/VideosDirPath")
    os.system(f' cd TiktokAutoUploader && ~/.pyenv/versions/3.10.14/envs/3.10-env/bin/python cli.py upload --user {tiktok_username} -v "{os.path.basename(video_path)}" -t "{title}" -sc {date}')

#upload_on_tiktok("test.mp4", "compte_test", "Video chpquate #fyp #cat ")