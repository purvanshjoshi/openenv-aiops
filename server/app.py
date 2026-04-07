import inspect
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openenv.core.env_server.http_server import create_app
from env import AIOpsEnv
from models import AIOpsAction, AIOpsObservation
import uvicorn

def create_aiops_env() -> AIOpsEnv:
    return AIOpsEnv()

app = create_app(
    create_aiops_env,
    AIOpsAction,
    AIOpsObservation,
    env_name="aiops_omni",
    max_concurrent_envs=1
)

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
