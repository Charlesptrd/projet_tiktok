from moviepy import VideoFileClip, vfx, ColorClip, ImageClip, AudioFileClip, CompositeAudioClip, afx
from moviepy import CompositeVideoClip
import datetime
import atexit, os


moment = None

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


def tiktok_style_video(URL, zoom, start_time, end_time):

    start_time = time_str_to_seconds(start_time)
    end_time = time_str_to_seconds(end_time)

    global moment
    moment=datetime.datetime.now()
    moment=moment.replace(microsecond=0)
    parse = f"downloads/{moment}.mp4"
    parse = parse.replace(":", "-").replace(" ", "_")
    parse_2 = f"downloads/CLEAN_{moment}.mp4"
    parse_2 = parse_2.replace(":", "-").replace(" ", "_")


    print(" ⛔️ Telechargement du clip")
    os.system(f'./TwitchDownloaderCLI videodownload --id "{URL}" -b {start_time} -e {end_time} -o "{parse}"')
    print(" ✅ Telechargement terminé")


    os.system(f"ffmpeg -i '{parse}' -map_chapters -1 -c copy '{parse_2}'")


    print(f"OUVERTURE de : '{parse_2}'")
    
    clip = VideoFileClip(f'{parse_2}')
    print("✅ OUVERTURE terminé")

    #audio = process_audio(clip)
    #clip = clip.with_audio(audio)


    clip_w, clip_h = clip.size

    target_w, target_h = 1080*1, 1920*1

    # === Fond : zoom + crop pour remplir l'écran vertical ===
    scale_bg = max(target_w / clip_w, target_h / clip_h)
    background = clip.with_effects([
        vfx.Resize(scale_bg),
        vfx.Crop(width=target_w, height=target_h)
    ]).with_position(("center", "center"))


    from moviepy.video.fx import HeadBlur
    def fx(t):
        return background.w * (t / background.duration)  # X position (center)
        
    def fy(t):
        return background.h * (t / background.duration)  # Y position (center)
        
    radius = 9999 # it is enough because it will crop on the video dimensions anyway
    background = background.with_effects([HeadBlur(fx,fy,radius, intensity=50)])

    # === Premier plan : largeur max = 1080px ===
    fg_scale = target_w*zoom / clip_w  # pour que width = 1080px
    foreground = clip.with_effects([
        vfx.Resize(fg_scale), vfx.MultiplyColor(1)
    ]).with_position(("center", 200))

    #filigranne INFLUPOSTEUR
    #filigranne = ImageClip("assets/filigranne.png") \
    #.with_duration(clip.duration) \
    #.with_position(("center", 590)) \
    #.with_opacity(0.3)  # 30% transparent
    
    #layer anti detection 
    #transparent_layer = ColorClip(size=(target_w, target_h), color=(0, 0, 0), duration=clip.duration).with_opacity(.2)

    # === Composite final ===
    final = CompositeVideoClip(
        [background, foreground],
        size=(target_w, target_h)
    )
    final = final.with_audio(clip.audio)


    # === Prévisualisation final ===
    #temp = final.subclipped(0, 1)
    #temp.preview()


    final.write_videofile(
        f"/Users/charles/Downloads/rendus/video_{moment}.mp4",
        fps=clip.fps,
        codec="libx264",
        audio_codec="aac",      # Codec audio compatible Mac/iPhone
        audio_bitrate="192k"   # Qualité audio
    )
    os.system(f"rm -f {parse}")
    os.system(f"rm -f {parse_2}")


tiktok_style_video("https://www.twitch.tv/videos/2520497010", 1.6, "01:13:08 ", "01:13:10")

atexit.register(cleanup)