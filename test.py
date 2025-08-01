from datetime import datetime
moment= datetime.now()
moment=moment.replace(microsecond=0)
print(f"✅ Tout est bon au : {moment}")