"""Scenes import the recorder from tools/; run each scene with python3 tools/scenes/NN_name.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
