import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000"

def run_memory_extraction():
    print("\n--- 1. RUNNING MEMORY EXTRACTION ON 30 MESSAGES ---")
    try:
        with open("demo_data.json", "r") as f:
            history = json.load(f)
        
        response = requests.post(f"{BASE_URL}/analyze", json={"history": history})
        
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            print("Error:", response.text)
    except FileNotFoundError:
        print("Error: demo_data.json not found. Please create it first.")

def run_personality_comparison():
    print("\n--- 2. RUNNING PERSONALITY ENGINE COMPARISON ---")
    test_message = "I failed my interview yesterday and I feel like giving up on this project."
    
    personas = ["calm_mentor", "witty_friend", "tech_bro", "minimalist"]
    
    print(f"User Message: '{test_message}'\n")
    
    for p in personas:
        demo_user_id = f"demo_user_{p}"
        
        payload = {
            "user_id": demo_user_id, 
            "message": test_message, 
            "persona": p
        }
        
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        
        if response.status_code == 200:
            reply = response.json()['response']
            print(f"[{p.upper()}]: {reply}\n")
        else:
            print(f"Error for {p}: {response.text}")

if __name__ == "__main__":
    try:
        run_memory_extraction()
        run_personality_comparison()
    except Exception as e:
        print(f"Ensure server is running! Error: {e}")