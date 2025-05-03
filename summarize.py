def run(arg=""):
    if not arg.strip():
        return "⚠️ Please provide some text to summarize."
    
    sentences = arg.split(".")
    if len(sentences) <= 2:
        return "📝 Summary: " + arg.strip()
    
    summary = sentences[0].strip() + ". " + sentences[-2].strip() + "."
    return f"📝 Summary: {summary}"
