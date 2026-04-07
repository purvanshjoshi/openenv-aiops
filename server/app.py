import inspect
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openenv.core.env_server.http_server import create_app
from env import AIOpsEnv
import uvicorn

app = create_app(
    EnvironmentClass=AIOpsEnv,
    max_concurrent_envs=1
)

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
