import zipfile
import os

def run(target_path):
    if not os.path.isdir(target_path):
        return f"❌ '{target_path}' is not a valid folder."

    zip_path = target_path + ".zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(target_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, target_path)
                zipf.write(full_path, arcname)
    
    return f"✅ Folder compressed to: {zip_path}"
