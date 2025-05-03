from datetime import datetime

def run(arg=""):
    now = datetime.now()
    return f"🕒 Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
