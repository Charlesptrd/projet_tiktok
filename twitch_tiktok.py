from moviepy import VideoFileClip, vfx, ColorClip, ImageClip, AudioFileClip, CompositeAudioClip, afx, TextClip
from moviepy import CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from datetime import datetime, timedelta
import atexit, os
from textwrap import fill
from upload import *
import sys, subprocess

FONT_PATH = "/Library/Fonts/Arial.ttf"  # ← à adapter selon ton système
TEXT_COLOR = "white"
FONT_SIZE = 50
LINE_WIDTH = 10
FACTOR = 1.04


moment = None

def get_executable_path(env="auto"):
    if env != "auto":
        return {
            "mac": "TwitchDownloaderCLI",
            "linux": "TwitchDownloaderCLI_Linux",
        }.get(env, "TwitchDownloaderCLI")
    else:
        return "TwitchDownloaderCLI"



def cleanup():
    global moment
    os.system(f"rm -f downloads/{moment}.mp4")
    os.system(f"rm -f downloads/CLEAN_{moment}.mp4")


def time_str_to_seconds(time_str):
    try:
        heure, minutes, seconds = map(int, time_str.strip().split(':'))
        return heure*3600 + minutes * 60 + seconds
    except ValueError:
        raise ValueError(f"Format invalide : '{time_str}'. Format attendu : 'm:s' (ex: '01:09:02')")


def process_audio(clip, noise_path="noise.mp3"):
    # 2. Réduire légèrement le volume (facultatif)
    audio = clip.audio

    # 3. Ajouter un fond sonore subtil si fourni
    if noise_path:
        noise = AudioFileClip(noise_path)
        noise = noise.with_duration(clip.duration)
        audio = CompositeAudioClip([audio, noise])

    return audio


def tiktok_style_video(URL, zoom, start_time, end_time, compte, titre, exe, music=None, start_music=0 ,is_test=0, ):
    os.system("rm -r -f downloads/*")
    os.system("echo On est la")

    start_time = time_str_to_seconds(start_time)
    end_time = time_str_to_seconds(end_time)
    delta = end_time-start_time +2
    start_time -= 2

    global moment
    moment= datetime.now()
    moment=moment.replace(microsecond=0)
    parse = f"downloads/{moment}.mp4"
    parse = parse.replace(":", "-").replace(" ", "_")
    parse_2 = f"downloads/CLEAN_{moment}.mp4"
    parse_2 = parse_2.replace(":", "-").replace(" ", "_")

    os.system("echo ⛔️ Telechargement du clip")

    subprocess.run(
    [f"./{exe}", "videodownload", "--id", URL, "-b", str(start_time), "-e", str(end_time), "-o", parse],
    stdout=sys.stdout,
    stderr=sys.stderr
)
    os.system("echo ✅ Telechargement terminé")
    os.system("echo ⛔️  Convertion du clip")

    subprocess.run(
    ["ffmpeg", "-i", parse, "-map_chapters", "-1", "-c", "copy", parse_2],
    stdout=sys.stdout,
    stderr=sys.stderr
)
    os.system("echo ✅ Convertion terminé\n")
    os.system(f"echo OUVERTURE de : '{parse_2}'")
    
    
    clip = VideoFileClip(f'{parse_2}').with_speed_scaled(factor=FACTOR)
    clip = clip.subclipped(2, clip.duration)
    os.system("echo ✅ OUVERTURE terminé")
    clip_w, clip_h = clip.size

    target_w, target_h = 1080*1, 1920*1

    """
    background = clip.with_effects([
        vfx.Resize(scale_bg),
        vfx.Crop(width=target_w, height=target_h)
    ]).with_position(("center", "center"))
    background = background.with_effects([HeadBlur(fx,fy,radius, intensity=50)])
    """
    background = VideoFileClip("assets/background2.mp4").subclipped(0, clip.duration)
    os.system("echo ✅ on a charfe larriere plan")
    # === Premier plan : largeur max = 1080px ===
    fg_scale = target_w*zoom / clip_w  # pour que width = 1080px
    foreground = clip.with_effects([
        vfx.Resize(fg_scale), vfx.MultiplyColor(1), vfx.Rotate(.3)
    ]).with_position(("center", 400))
    os.system("echo ✅ premier plann")
    #filigranne INFLUPOSTEUR
    filigranne = ImageClip("assets/filigranne.png") \
    .with_duration(clip.duration) \
    .with_position(("center", 800)) \
    .with_opacity(0.4)  # 30% transparent
    os.system("echo ✅ filigranne")
    """
    #Bas d'immage Influfloppeur.
    bas = ImageClip("assets/image2.png") \
    .with_duration(clip.duration) \
    .with_position(("center", 1380)).resized(width=1080)
    """
    #layer anti detection 
    transparent_layer = ColorClip(size=(target_w, target_h), color=(0, 0, 0), duration=clip.duration).with_opacity(.1)
    os.system("echo ✅ transparence")

    if is_test == 2:
        final = CompositeVideoClip(
            [foreground],
            size=(target_w, target_h)
        )
    else:
        # === Composite final ===
        final = CompositeVideoClip(
            [background, foreground, transparent_layer, filigranne],
            size=(target_w, target_h)
        )
    os.system("echo ✅ Composite")


    

    if music != None:
        audio = AudioFileClip(music).with_effects([afx.MultiplyVolume(0.07)])
        audio = audio.subclipped(start_music, final.duration+start_music)
        mixed = CompositeAudioClip([clip.audio, audio])
        final = final.with_audio(mixed)
    else:
        final = final.with_audio(clip.audio)
    
    os.system("echo ✅ musique")
    #if exe == "TwitchDownloaderCLI":
        # === Prévisualisation final ===
        #temp = final.subclipped(0, 1)
        #temp.preview()

    name_temps = f"rendus/video_{moment}.mp4"
    name_temps = name_temps.replace(":", "-").replace(" ", "_")

    os.system("echo ✅ on va charger le rendu")
    output_dir = "rendus"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    final.write_videofile(
        f"{name_temps}",
        fps=clip.fps,
        codec="libx264",
        audio_codec="aac",      # Codec audio compatible Mac/iPhone
        audio_bitrate="192k"   # Qualité audio
    )
    os.system("echo ✅ rendu ecrit")

    if is_test == 0 :
        upload_on_tiktok(f"{name_temps}", compte, titre)
        caca = 0
    os.system("echo ✅ Uppload fait")
env = sys.argv[1] if len(sys.argv) > 1 else "auto"
exe = get_executable_path(env)
os.chmod(exe, 0o755)

#tiktok_style_video("https://www.twitch.tv/videos/2524068137", 1.6, "4:17:23", "4:17:40", "vrai_compte_2", "Anyme le dictateur", "musics/sneaky.mp3", is_test=0, start_music=0)

#tiktok_style_video("https://www.twitch.tv/videos/2527578233", 1.6, "00:07:52", "00:08:10", "vrai_compte_2", "Anyme menace le fils du proprio", "musics/sad.mp3", is_test=0, start_music=0)#tiktok_style_video("https://www.twitch.tv/videos/2527578233", 1.6, "00:07:52", "00:08:10", "vrai_compte_2", "Anyme menace le fils du proprio", "musics/sad.mp3", is_test=0, start_music=0)
tiktok_style_video("https://www.twitch.tv/videos/2527578233", 1.6, "00:18:38", "00:18:45", "compte_test", "Anyme étienne", exe, music="musics/sneaky.mp3", is_test=0, start_music=0)

atexit.register(cleanup)