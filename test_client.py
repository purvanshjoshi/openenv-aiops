import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print(f"--- Simulating Agent solving 'Easy' Task ---")
    
    # 1. Reset Environment for 'easy' task
    print("\n[Client] Sending POST /reset (Task: 'easy')")
    try:
        res = requests.post(f"{BASE_URL}/reset", json={"task_name": "easy"})
        res.raise_for_status()
        state = res.json()
        print(f"[Server Response] Observation: {json.dumps(state.get('observation', {}), indent=2)}")
    except Exception as e:
        print(f"Error connecting to server. Is it fully booted? {e}")
        return

    # 2. Agent Action 1: Query Billing
    action_1 = {
        "action": {
            "command": "query_billing",
            "parameters": {}
        }
    }
    print("\n[Client] Agent decided to check the billing records.")
    print(f"[Client] Sending POST /step: {json.dumps(action_1)}")
    res = requests.post(f"{BASE_URL}/step", json=action_1)
    step1 = res.json()
    print(f"[Server Response] Reward: {step1.get('reward')}")
    print(f"[Server Response] New Telemetry: {step1.get('observation', {}).get('telemetry_output')}")
    
    # 3. Agent Action 2: Refund the correct amount
    action_2 = {
        "action": {
            "command": "refund",
            "parameters": {"amount": 50}
        }
    }
    print("\n[Client] Agent found duplicate $50 charge, issuing refund.")
    print(f"[Client] Sending POST /step: {json.dumps(action_2)}")
    res = requests.post(f"{BASE_URL}/step", json=action_2)
    step2 = res.json()
    print(f"[Server Response] Reward: {step2.get('reward')}")
    print(f"[Server Response] New Telemetry: {step2.get('observation', {}).get('telemetry_output')}")
    
    # 4. Agent Action 3: Resolve Ticket
    action_3 = {
        "action": {
            "command": "resolve",
            "parameters": {}
        }
    }
    print("\n[Client] Task complete, closing ticket.")
    print(f"[Client] Sending POST /step: {json.dumps(action_3)}")
    res = requests.post(f"{BASE_URL}/step", json=action_3)
    step3 = res.json()
    print(f"[Server Response] Reward: {step3.get('reward')} | Done: {step3.get('done')}")

if __name__ == "__main__":
    # give server a small buffer
    time.sleep(1)
    test_api()
