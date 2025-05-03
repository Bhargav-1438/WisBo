def run(arg=""):
    if not arg.strip():
        return "⚠️ Please provide a sentence to count words."
    word_count = len(arg.strip().split())
    return f"🧮 Word Count: {word_count}"
