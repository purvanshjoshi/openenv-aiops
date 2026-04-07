import os
import json
from typing import List
from openai import OpenAI
from env import AIOpsEnv
from models import AIOpsAction

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy-token")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}")

def log_step(step: int, action: str, reward: float, done: bool, error: str):
    done_str = "true" if done else "false"
    err_str = error if error is not None else "null"
    action_str = action.replace("\n", " ").strip()
    print(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={done_str} error={err_str}")

def log_end(success: bool, steps: int, rewards: list):
    suc_str = "true" if success else "false"
    rews = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={suc_str} steps={steps} rewards={rews}")

SYSTEM_PROMPT = """You are an AIOps SRE Agent. 
You must output exactly ONE JSON action per turn.
Format: {"command": "...", "parameters": {"key": "value"}}
Commands: ["query_billing", "refund", "resolve"] for FinOps; ["query_data", "patch_data", "resolve"] for Compliance; ["analyze_fleet", "terminate_node", "resolve"] for Infra.
Parameters map to command requirements (e.g. "amount" for refund, "data" for patch string, "node_id" for terminate).
Always end with {"command": "resolve", "parameters": {}} after completing the task."""

def run_task(task_name: str):
    env = AIOpsEnv()
    obs = env.reset(task_name)
    
    steps_taken = 0
    rewards = []
    error = None
    
    log_start(task=task_name, env="aiops_omni", model=MODEL_NAME)
    
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        steps_taken += 1
        
        # Build state prompt
        obs_state = f"Incident: {obs.incident_description}\nTelemetry: {obs.telemetry_output}"
        history.append({"role": "user", "content": obs_state})
        
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=history,
            )
            raw_action = response.choices[0].message.content
            # VERY simple parse handling
            action_json = json.loads(raw_action)
            action = AIOpsAction(command=action_json["command"], parameters=action_json.get("parameters", {}))
            error = None
        except Exception as e:
            raw_action = "fallback_resolve"
            action = AIOpsAction(command="resolve", parameters={})
            error = str(e)
            
        history.append({"role": "assistant", "content": raw_action})
        
        obs = env.step(action)
        reward = obs.reward or 0.0
        done = obs.done
        
        rewards.append(reward)
        
        log_step(step=steps_taken, action=raw_action, reward=reward, done=done, error=error)
        
        if done or steps_taken >= 10:
            break
            
    score = sum(rewards)
    success = score > 0.0
    log_end(success=success, steps=steps_taken, rewards=rewards)

if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_task(task)
