def run(file_path="notes.txt"):
    try:
        with open(file_path, 'r') as file:
            return f"📖 Notes:\n\n{file.read()}"
    except Exception as e:
        return f"❌ Failed to read file: {e}"
