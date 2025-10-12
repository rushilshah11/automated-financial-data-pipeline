import sys
from pathlib import Path

# add project root to sys.path so `from main import app` works
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
