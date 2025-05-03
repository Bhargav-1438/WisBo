# test_connector.py

from core_engine import ask_wisbo, switch_mode, get_memory

def main():
    print("\n--- WisBo Test Session Start ---")

    # Step 1: Ask something
    print("\n[1] Asking WisBo a question...")
    response = ask_wisbo("What is the capital of France?", mode="default")
    print("WisBo Response:", response)

    # Step 2: Switch mode
    print("\n[2] Switching interaction mode to 'casual'...")
    mode_result = switch_mode("casual")
    print("Switched Mode:", mode_result)

    # Step 3: Get memory snapshot
    print("\n[3] Retrieving memory snapshot...")
    memory_data = get_memory()
    print("Memory Snapshot:", memory_data)

    print("\n--- WisBo Test Session End ---")

if __name__ == "__main__":
    main()
