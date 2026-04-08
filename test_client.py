import requests
import json
import time

BASE_URL = "http://localhost:7860"

def test_medium():
    print(f"\n{'='*50}\n--- Simulating Agent solving 'Medium' Task ---\n{'='*50}")
    
    res = requests.post(f"{BASE_URL}/reset", json={"task_name": "medium"})
    print(f"[Server Response] Observation:\n{json.dumps(res.json().get('observation', {}), indent=2)}")
    
    print("\n[Client] Sending POST /step (query_data)")
    res = requests.post(f"{BASE_URL}/step", json={"action": {"command": "query_data", "parameters": {}}})
    step1 = res.json()
    print(f"[Server Telemetry]: {step1.get('observation', {}).get('telemetry_output')}")
    
    print("\n[Client] Sending POST /step (patch_data -> anonymize PII)")
    res = requests.post(f"{BASE_URL}/step", json={"action": {"command": "patch_data", "parameters": {"data": "Patient [REDACTED] arrived at 9AM."}}})
    step2 = res.json()
    print(f"[Server Reward]: {step2.get('reward')} | [Telemetry]: {step2.get('observation', {}).get('telemetry_output')}")
    
    print("\n[Client] Sending POST /step (resolve)")
    res = requests.post(f"{BASE_URL}/step", json={"action": {"command": "resolve", "parameters": {}}})
    step3 = res.json()
    print(f"[Server Reward]: {step3.get('reward')} | Done: {step3.get('done')}")

def test_hard():
    print(f"\n{'='*50}\n--- Simulating Agent solving 'Hard' Task ---\n{'='*50}")
    
    res = requests.post(f"{BASE_URL}/reset", json={"task_name": "hard"})
    print(f"[Server Response] Incident:\n{res.json().get('observation', {}).get('incident_description')}")
    
    print("\n[Client] Sending POST /step (analyze_fleet)")
    res = requests.post(f"{BASE_URL}/step", json={"action": {"command": "analyze_fleet", "parameters": {}}})
    step1 = res.json()
    print(f"[Server Telemetry]: {step1.get('observation', {}).get('telemetry_output')}")
    
    print("\n[Client] Sending POST /step (terminate_node -> kill node-2 zombie)")
    res = requests.post(f"{BASE_URL}/step", json={"action": {"command": "terminate_node", "parameters": {"node_id": "node-2"}}})
    step2 = res.json()
    print(f"[Server Reward]: {step2.get('reward')} | [Telemetry]: {step2.get('observation', {}).get('telemetry_output')}")
    
    print("\n[Client] Sending POST /step (resolve)")
    res = requests.post(f"{BASE_URL}/step", json={"action": {"command": "resolve", "parameters": {}}})
    step3 = res.json()
    print(f"[Server Reward]: {step3.get('reward')} | Done: {step3.get('done')}")

if __name__ == "__main__":
    test_medium()
    time.sleep(1)
    test_hard()
