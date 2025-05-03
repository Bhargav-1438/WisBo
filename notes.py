import os
import json

NOTES_FILE = "brain/notes.json"

# Ensure notes file exists
os.makedirs("brain", exist_ok=True)
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w") as f:
        json.dump([], f)

def run(arg=""):
    if arg.strip().lower() == "show":
        with open(NOTES_FILE, "r") as f:
            notes = json.load(f)
        if not notes:
            return "🗒️ No notes yet."
        return "\n".join([f"- {n}" for n in notes])
    
    with open(NOTES_FILE, "r+") as f:
        notes = json.load(f)
        notes.append(arg)
        f.seek(0)
        json.dump(notes, f, indent=2)
    return f"✅ Note added: {arg}"
