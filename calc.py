def run(arg=""):
    try:
        result = eval(arg, {"__builtins__": {}}, {})
        return f"🧮 Result: {result}"
    except Exception as e:
        return f"❌ Calculation error: {e}"
