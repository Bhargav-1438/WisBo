import requests

BASE_URL = "http://127.0.0.1:8000"

def ask_wisbo(message: str, mode: str = "casual"):
    try:
        response = requests.post(f"{BASE_URL}/ask", json={"message": message, "mode": mode})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"WisBo core failed: {str(e)}"}

def switch_mode(new_mode: str):
    try:
        response = requests.post(f"{BASE_URL}/switch-mode", json={"mode": new_mode})
        return response.json()
    except Exception as e:
        return {"error": f"Failed to switch mode: {str(e)}"}

def get_memory():
    try:
        response = requests.get(f"{BASE_URL}/memory")
        return response.json()
    except Exception as e:
        return {"error": f"Failed to get memory: {str(e)}"}
