import sys
from pathlib import Path

# Ensure the package under development is importable without installation.
ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SRC = ROOT / "python" / "os_gravity_collapse" / "src"
if str(PACKAGE_SRC) not in sys.path:
    sys.path.insert(0, str(PACKAGE_SRC))
