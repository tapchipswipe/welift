import sys
from pathlib import Path

# Add parent directory to sys.path for root module imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from main import app
