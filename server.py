import inspect
from fastapi import FastAPI
from openenv.core.env_server.http_server import create_app
from env import AIOpsEnv
from models import AIOpsAction, AIOpsObservation

def create_aiops_env() -> AIOpsEnv:
    return AIOpsEnv()

app = create_app(
    create_aiops_env,
    AIOpsAction,
    AIOpsObservation,
    env_name="aiops_omni",
    max_concurrent_envs=1
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
