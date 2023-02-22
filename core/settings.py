from dotenv import load_dotenv
from pathlib import Path


def environment_config():
    env_path = Path('.') / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
