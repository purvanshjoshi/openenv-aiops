import requests
import json
import time

BASE_URL = "https://purvansh01-openenv-aiops.hf.space"

s = requests.Session()

def test_medium():
    print(f"\n{'='*50}\n--- Simulating Agent solving 'Medium' Task ---\n{'='*50}")
    
    res = s.post(f"{BASE_URL}/reset", json={"task_name": "medium"})
    data = res.json()
    print(f"DEBUG Reset Response: {data}")
    total_reward = data.get("reward", 0.0)
    print(f"[Reset Reward]: {total_reward}")
    
    print("\n[Client] Sending POST /step (query_data)")
    res = s.post(f"{BASE_URL}/step", json={"action": {"command": "query_data", "parameters": {}}})
    step1 = res.json()
    print(f"DEBUG Step 1 Response: {step1}")
    total_reward += step1.get("reward", 0.0)
    print(f"[Step 1 Reward]: {step1.get('reward')} | Cumulative: {total_reward:.2f}")
    
    print("\n[Client] Sending POST /step (patch_data -> anonymize PII)")
    res = s.post(f"{BASE_URL}/step", json={"action": {"command": "patch_data", "parameters": {"data": "Patient [REDACTED] arrived at 9AM."}}})
    step2 = res.json()
    total_reward += step2.get("reward", 0.0)
    print(f"[Step 2 Reward]: {step2.get('reward')} | Cumulative: {total_reward:.2f}")
    
    print("\n[Client] Sending POST /step (resolve)")
    res = s.post(f"{BASE_URL}/step", json={"action": {"command": "resolve", "parameters": {}}})
    step3 = res.json()
    total_reward += step3.get("reward", 0.0)
    print(f"[Step 3 Reward]: {step3.get('reward')} | Total Score: {total_reward:.2f}")

def test_hard():
    print(f"\n{'='*50}\n--- Simulating Agent solving 'Hard' Task ---\n{'='*50}")
    
    res = s.post(f"{BASE_URL}/reset", json={"task_name": "hard"})
    data = res.json()
    total_reward = data.get("reward", 0.0)
    print(f"[Reset Reward]: {total_reward}")
    
    print("\n[Client] Sending POST /step (analyze_fleet)")
    res = s.post(f"{BASE_URL}/step", json={"action": {"command": "analyze_fleet", "parameters": {}}})
    step1 = res.json()
    total_reward += step1.get("reward", 0.0)
    print(f"[Step 1 Reward]: {step1.get('reward')} | Cumulative: {total_reward:.2f}")
    
    print("\n[Client] Sending POST /step (terminate_node -> kill node-2 zombie)")
    res = s.post(f"{BASE_URL}/step", json={"action": {"command": "terminate_node", "parameters": {"node_id": "node-2"}}})
    step2 = res.json()
    total_reward += step2.get("reward", 0.0)
    print(f"[Step 2 Reward]: {step2.get('reward')} | Cumulative: {total_reward:.2f}")
    
    print("\n[Client] Sending POST /step (resolve)")
    res = s.post(f"{BASE_URL}/step", json={"action": {"command": "resolve", "parameters": {}}})
    step3 = res.json()
    total_reward += step3.get("reward", 0.0)
    print(f"[Step 3 Reward]: {step3.get('reward')} | Total Score: {total_reward:.2f}")

if __name__ == "__main__":
    test_medium()
    time.sleep(1)
    test_hard()
