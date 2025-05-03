# test_fallback.py

from core_engine import ask_wisbo

# Simulate asking a question — fallback will trigger if local server fails
try:
    question = "Explain quantum entanglement"
    print(f"Asking: {question}")
    response = ask_wisbo(question, mode="casual")
    print("WisBo Response:", response)
except Exception as e:
    print("Error during fallback test:", e)
