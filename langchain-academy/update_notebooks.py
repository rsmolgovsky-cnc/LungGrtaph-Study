#!/usr/bin/env python3
"""Update all notebooks with dotenv loading and langgraph up (Docker-based)."""
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent

# Cell to add for dotenv loading
DOTENV_CELL: dict[str, Any] = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Load environment variables from .env file\n",
        "from dotenv import load_dotenv\n",
        "from pathlib import Path\n",
        "\n",
        "# Find and load .env from project root\n",
        "env_path = Path('.').resolve()\n",
        "while env_path != env_path.parent:\n",
        "    if (env_path / '.env').exists():\n",
        "        load_dotenv(env_path / '.env')\n",
        "        break\n",
        "    env_path = env_path.parent"
    ]
}

def update_notebook(notebook_path: Path) -> tuple[bool, bool]:
    """Update a single notebook. Returns (dotenv_added, langgraph_updated)."""
    with open(notebook_path, 'r') as f:
        nb = json.load(f)

    dotenv_added = False
    langgraph_updated = False

    cells = nb.get('cells', [])

    # Check if dotenv is already loaded
    has_dotenv = any(
        'load_dotenv' in ''.join(cell.get('source', []))
        for cell in cells
    )

    # Find pip install cell and insert dotenv cell after it
    if not has_dotenv:
        for i, cell in enumerate(cells):
            source = ''.join(cell.get('source', []))
            if '%pip install' in source or 'pip install' in source:
                # Insert dotenv cell after pip install
                # Give it a unique id
                dotenv_cell = DOTENV_CELL.copy()
                dotenv_cell['id'] = f'dotenv-load-{i}'
                cells.insert(i + 1, dotenv_cell)
                dotenv_added = True
                break

    # Update langgraph dev to langgraph up (Docker-based)
    for cell in cells:
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            if isinstance(source, list):
                new_source = []
                for line in source:
                    if 'langgraph dev' in line and 'langgraph up' not in line:
                        # Replace langgraph dev with langgraph up
                        line = line.replace('langgraph dev', 'langgraph up')
                        langgraph_updated = True
                    new_source.append(line)
                cell['source'] = new_source
            elif isinstance(source, str):
                if 'langgraph dev' in source and 'langgraph up' not in source:
                    cell['source'] = source.replace('langgraph dev', 'langgraph up')
                    langgraph_updated = True

    nb['cells'] = cells

    # Write back
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)

    return dotenv_added, langgraph_updated


def main() -> None:
    notebooks = list(PROJECT_ROOT.glob('**/*.ipynb'))
    print(f"Found {len(notebooks)} notebooks")

    dotenv_count = 0
    langgraph_count = 0

    for nb_path in notebooks:
        dotenv_added, langgraph_updated = update_notebook(nb_path)
        if dotenv_added:
            dotenv_count += 1
            print(f"  Added dotenv: {nb_path.relative_to(PROJECT_ROOT)}")
        if langgraph_updated:
            langgraph_count += 1
            print(f"  Updated to langgraph up: {nb_path.relative_to(PROJECT_ROOT)}")

    print(f"\nSummary:")
    print(f"  Dotenv added to {dotenv_count} notebooks")
    print(f"  Changed to langgraph up in {langgraph_count} notebooks")


if __name__ == "__main__":
    main()
