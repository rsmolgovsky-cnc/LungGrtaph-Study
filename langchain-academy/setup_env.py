"""
Load environment variables from .env file.

In any notebook, add this cell at the top:

    import sys
    sys.path.insert(0, '..')  # or '../..' depending on depth
    from setup_env import load_env
    load_env()

Or simpler - just run this in a notebook cell:

    from dotenv import load_dotenv
    load_dotenv('../.env')  # adjust path as needed
"""
import os
from pathlib import Path
from typing import Union

def load_env(env_path: Union[str, Path, None] = None) -> None:
    """Load environment variables from .env file.

    Args:
        env_path: Path to .env file. If None, searches up the directory tree.
    """
    from dotenv import load_dotenv

    if env_path:
        env_file = Path(env_path)
    else:
        # Search up directory tree for .env
        current = Path.cwd()
        env_file = None
        for parent in [current] + list(current.parents):
            candidate = parent / ".env"
            if candidate.exists():
                env_file = candidate
                break

    if env_file and env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded environment from {env_file}")
    else:
        print("Warning: .env file not found")
        return

    # Verify key variables are set
    required = ["LANGSMITH_API_KEY"]
    missing = [v for v in required if not os.environ.get(v) or os.environ.get(v) == "your-api-key-here"]

    if missing:
        print(f"Please set these in .env: {missing}")
    else:
        print("Environment configured successfully")

if __name__ == "__main__":
    load_env()
