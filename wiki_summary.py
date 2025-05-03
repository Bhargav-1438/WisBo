import requests

def run(topic):
    if not topic:
        return "❗ Please provide a topic to summarize."

    try:
        response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}")
        data = response.json()

        if "extract" in data:
            return f"📘 {data['title']}:\n{data['extract']}"
        else:
            return "❌ Could not find a summary for that topic."
    except Exception as e:
        return f"⚠️ Error fetching summary: {e}"
