import requests

# === Config ===
# You can switch these later from your main code or via an env file
DEFAULT_MODEL_NAME = "Meta-Llama-3-8B-Instruct-GGUF"
DEFAULT_MODEL_ENDPOINT = "http://localhost:1234/v1/chat/completions"
DEFAULT_TEMPERATURE = 0.7

# === Main LLM Handler ===
def query_model(prompt, memory_context=None, mode="default", system_prompt=""):
    """
    Sends a prompt to the model endpoint with optional memory context and system message.
    """

    messages = [{"role": "system", "content": system_prompt}]
    
    if memory_context:
        for entry in memory_context:
            messages.append({"role": "user", "content": entry["prompt"]})
            messages.append({"role": "assistant", "content": entry["response"]})
    
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": DEFAULT_MODEL_NAME,
        "messages": messages,
        "temperature": DEFAULT_TEMPERATURE
    }

    try:
        response = requests.post(DEFAULT_MODEL_ENDPOINT, json=payload)
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[Error] Model request failed: {e}"
