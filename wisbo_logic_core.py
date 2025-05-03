import os
import json
import datetime
import requests
import importlib.util

# === Force working directory to the script's folder ===
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# === Config ===
MEMORY_DIR = "brain"
BOOKMARKS_FILE = os.path.join(MEMORY_DIR, "bookmarks.json")
SESSIONS_DIR = "sessions"
MODEL_ENDPOINT = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "Meta-Llama-3-8B-Instruct-GGUF"
SUMMARIES_FILE = os.path.join(SESSIONS_DIR, "summaries.json")

# === Ensure folders & files ===
os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(SESSIONS_DIR, exist_ok=True)
os.makedirs("tools", exist_ok=True)

# Create empty bookmarks and summaries if not exist
if not os.path.exists(BOOKMARKS_FILE):
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(SUMMARIES_FILE):
    with open(SUMMARIES_FILE, "w") as f:
        json.dump({}, f)
        
# === Mode Greetings ===
mode_greetings = {
    "coach": "💪 Let's crush it together!",
    "tactician": "🎯 Tactical mode engaged. Objective: clarity.",
    "sarcastic": "🙄 Great. Another question. Let’s gooo...",
    "default": "🤖 WisBo Core mode. Logic optimized."
}
# === Mode Response Prefixes ===
def get_response_prefix(mode):
    prefixes = {
        "coach": "🏋️‍♂️ WisBo (Coach):",
        "tactician": "🧠 WisBo (Tactician):",
        "sarcastic": "😒 WisBo (Sassy):",
        "default": "🤖 WisBo:"
    }
    return prefixes.get(mode, "🤖 WisBo:")


# === Personality System ===
def get_system_prompt(mode):
    prompts = {
        "coach": "You are WisBo the Motivational Coach. Give practical support and encouragement.",
        "tactician": "You are WisBo the Tactical Planner. Break tasks sharply like a mission plan.",
        "sarcastic": "You are WisBo the Sarcastic Assistant. Help but with snarky humor.",
        "default": "You are WisBo Core v0.9.4 — a logical and resourceful assistant."
    }
    return prompts.get(mode, prompts["default"])

# === Memory System (Per Mode) ===
def get_memory_path(mode):
    return os.path.join(MEMORY_DIR, f"memory_{mode}.json")

def log_interaction(prompt, response, mode="default"):
    path = get_memory_path(mode)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
    with open(path, "r+") as f:
        data = json.load(f)
        data.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "prompt": prompt,
            "response": response
        })
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

def recall_context(limit=3, mode_filter="default"):
    path = get_memory_path(mode_filter)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        data = json.load(f)
        return data[-limit:] if data else []

def clear_memory(mode):
    path = get_memory_path(mode)
    with open(path, "w") as f:
        json.dump([], f)

# === Bookmark System ===
def save_bookmark(keyword, info):
    with open(BOOKMARKS_FILE, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
        data[keyword.lower()] = info
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

def get_bookmark(keyword):
    with open(BOOKMARKS_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None
        return data.get(keyword.lower())

# === Tool System ===
# === Tool System: Upgraded Execution ===
def execute_tool_command(command):
    if not command.lower().startswith("run:"):
        return None

    parts = command[4:].strip().split(" ", 1)
    tool_name = parts[0]
    arg = parts[1] if len(parts) > 1 else ""
    tool_path = os.path.join("tools", f"{tool_name}.py")

    if not os.path.isfile(tool_path):
        return f"❌ Tool '{tool_name}' not found in /tools folder."

    try:
        spec = importlib.util.spec_from_file_location("tool", tool_path)
        tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tool)

        if not hasattr(tool, "run"):
            return f"⚠️ Tool '{tool_name}' does not define a 'run(arg)' function."

        return tool.run(arg)

    except Exception as e:
        return f"❌ Tool '{tool_name}' failed to execute:\n> {e}"

# === JARVIS ROUTING SYSTEM ===
def jarvis_router(prompt):
    lowered = prompt.lower()

    # 1. Time Check
    if any(word in lowered for word in ["time", "clock", "what time is it"]):
        return execute_tool_command("run: clock")

    # 2. Word Counter
    if "how many words" in lowered:
        sentence = prompt.split("words", 1)[-1].strip()
        return execute_tool_command(f"run: count_words {sentence}")

    # 3. Folder Compression
    if "compress" in lowered and "folder" in lowered:
        import re
        match = re.search(r"compress.*folder\s+(.*)", lowered)
        if match:
            folder_name = match.group(1)
            return execute_tool_command(f"run: compress_folder {folder_name}")
        else:
            return "📁 Please specify a folder name to compress."
        # 4. Text Summarization
    if "summarize" in lowered:
        import re
        match = re.search(r"summarize(.*)", prompt, re.IGNORECASE)
        if match:
            text = match.group(1).strip()
            if text:
                return execute_tool_command(f"run: summarize {text}")
            else:
                return "📝 Please provide the text to summarize."
                # 5. Wikipedia Summary
    if "wikipedia" in lowered or "tell me about" in lowered:
        import re
        match = re.search(r"(wikipedia|tell me about)\s+(.*)", lowered)
        if match:
            topic = match.group(2).strip().replace(" ", "_")
            return execute_tool_command(f"run: wiki_summary {topic}")
        else:
            return "🔍 Please provide a topic to search."


    # Default → not routed, send to LLM
    return None

# === LLM Interaction ===
def ask_wisbo(prompt, mode="default"):
    memory_context = recall_context(limit=3, mode_filter=mode)
    messages = [{"role": "system", "content": get_system_prompt(mode)}]
    
    for mem in memory_context:
        messages.append({"role": "user", "content": mem["prompt"]})
        messages.append({"role": "assistant", "content": mem["response"]})
    
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(MODEL_ENDPOINT, json=payload)
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[Error] Could not reach model: {e}"

# === Session Logger ===
current_session_path = None

def log_to_session(prompt, response):
    if not current_session_path:
        return
    with open(current_session_path, "r+") as f:
        data = json.load(f)
        data.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "prompt": prompt,
            "response": response
        })
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
        

# === CLI Start ===
print("\n🤖 WisBo Core v0.9.4 — Hybrid Mode Activated!")
print("➡ Type commands like:")
print("  - 'mode: coach/tactician/sarcastic/default' to switch AI style.")
print("  - 'run: toolname [arg]' to run tools from /tools folder.")
print("  - 'list tools' to list available tools.")
print("  - 'list sessions' to list past sessions.")
print("  - 'recall session: session_filename' to load a session.")
print("  - 'recall' to show memory, 'clear memory' to reset.")
print("  - 'save: keyword -> info' to save bookmarks.")
print("  - 'remember: keyword' to fetch bookmarks.")
print("  - 'exit' to quit WisBo.\n")

# === Start a new session file ===
session_time = datetime.datetime.now().isoformat().replace(":", "-")
current_session_path = os.path.join(SESSIONS_DIR, f"session_{session_time}.json")
with open(current_session_path, "w") as f:
    json.dump([], f)

# Save summary
summary = input("📝 Enter a short summary for this session: ").strip()
session_name = os.path.basename(current_session_path)
with open(SUMMARIES_FILE, "r+") as f:
    data = json.load(f)
    data[session_name] = summary
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
print(f"✅ Summary saved for session '{session_name}'.")

current_mode = "default"

# === Main CLI Loop ===
while True:
    user_input = input("You: ").strip()

    # === Friendly Exit ===
    if user_input.lower() in ["exit", "quit"]:
        if current_mode == "coach":
            print("👋 WisBo Coach: Proud of your progress today! See you next session!")
        elif current_mode == "tactician":
            print("🎯 WisBo Tactician: Strategy saved. Until next operation!")
        elif current_mode == "sarcastic":
            print("🙄 WisBo Sarcastic: Finally! I thought you'd never leave. Bye!")
        else:
            print("👋 WisBo: Goodbye! Stay awesome!")
        break

    # === Mode Switch ===
    # === Mode Switch with Personality Greeting ===
    if user_input.lower().startswith("mode:"):
     new_mode = user_input.split("mode:")[1].strip().lower()
    if new_mode in ["default", "coach", "tactician", "sarcastic"]:
        current_mode = new_mode
        greeting = mode_greetings.get(current_mode, "🧠 Mode changed.")
        print(f"🧠 Mode switched to '{current_mode}'.")
        print(f"{greeting}")
    else:
        print("❌ Unknown mode.")
        continue


    # === Recall Memory ===
    if user_input.lower() == "recall":
        past = recall_context(limit=5, mode_filter=current_mode)
        if not past:
            print("📭 No recent memory found.")
        else:
            print(f"🧠 Memory from '{current_mode}' mode:")
            for item in past:
                print(f"- {item['prompt']} → {item['response']}")
        continue

    # === Clear Memory ===
    if user_input.lower() == "clear memory":
        clear_memory(current_mode)
        print(f"🧹 Memory for '{current_mode}' cleared.")
        continue

    # === List Sessions ===
    if user_input.lower() == "list sessions":
        try:
            with open(SUMMARIES_FILE, "r") as f:
                data = json.load(f)
            if not data:
                print("📭 No saved sessions yet.")
            else:
                print("🗂 Saved Sessions:")
                for name, summary in data.items():
                    print(f"- {name}: {summary}")
        except Exception as e:
            print(f"❌ Error reading sessions: {e}")
        continue

    # === Recall a Specific Session ===
    if user_input.lower().startswith("recall session:"):
        session_file = user_input.split("recall session:", 1)[1].strip()
        session_path = os.path.join(SESSIONS_DIR, session_file)

        if not os.path.exists(session_path):
            print(f"📭 No such session file '{session_file}'.")
            continue

        try:
            with open(session_path, "r") as f:
                session_data = json.load(f)
            
            print(f"🧠 Full conversation from '{session_file}':")
            for entry in session_data:
                print(f"- {entry['prompt']} → {entry['response']}")
        except Exception as e:
            print(f"❌ Error reading session: {e}")
        continue

    # === Tool Commands ===
    if user_input.lower().startswith("run:"):
        result = execute_tool_command(user_input)
        print(result if result else "✅ Tool executed successfully.")
        continue

    # === Bookmark Commands ===
    if user_input.lower().startswith("save:"):
        try:
            keyword, info = user_input[5:].split("->")
            keyword, info = keyword.strip(), info.strip()
            save_bookmark(keyword, info)
            print(f"🔖 Bookmark saved: '{keyword}' → {info}")
        except ValueError:
            print("❌ Invalid save format. Use: save: keyword -> info.")
        continue

    if user_input.lower().startswith("remember:"):
        keyword = user_input[9:].strip()
        info = get_bookmark(keyword)
        if info:
            print(f"🔖 Bookmark for '{keyword}': {info}")
        else:
            print(f"📭 No bookmark found for '{keyword}'.")
        continue
    # === List Available Tools ===
    if user_input.lower() == "list tools":
       try:
        tool_list = [
            f[:-3] for f in os.listdir("tools")
            if f.endswith(".py") and not f.startswith("__")
        ]
        if not tool_list:
            print("🧰 No tools found.")
        else:
            print("🧰 Available Tools:")
            for tool in tool_list:
                print(f"- {tool}")
       except Exception as e:
        print(f"❌ Error reading tools: {e}")
       continue
    
    # === JARVIS SMART ROUTING ===
    routed_response = jarvis_router(user_input)
    if routed_response:
        print(f"{get_response_prefix(current_mode)} {routed_response}")
        log_interaction(user_input, routed_response, mode=current_mode)
        log_to_session(user_input, routed_response)
        continue

    # === Default: Query WisBo ===
    print("🧠 Thinking... Please wait.")
    response = ask_wisbo(user_input, mode=current_mode)
    print(f"{get_response_prefix(current_mode)} {response}")
    log_interaction(user_input, response, mode=current_mode)
    log_to_session(user_input, response)
