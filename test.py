import os
from datetime import datetime

moment= datetime.now()
moment=moment.replace(microsecond=0)
parse = f"downloads/{moment}.%(ext)s"
parse = parse.replace(":", "-").replace(" ", "_")

URL = "https://www.youtube.com/watch?v=ap-S1gCTs6I"

start_time = "00:00:00"
end_time = "00:00:10"

#os.system(f'yt-dlp -f bestvideo+bestaudio --download-sections "*{start_time}-{end_time}" -o "{parse}" --recode-video mp4 "{URL}" ')
os.system(f'yt-dlp -f bestvideo+bestaudio --download-sections "*{start_time}-{end_time}" -o "{parse}" --recode-video mp4 "{URL}"')