from datetime import datetime

def run(arg=""):
    now = datetime.now()
    return f"🕒 Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
