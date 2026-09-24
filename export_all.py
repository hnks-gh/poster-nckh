"""Root entry point for exporting all poster assets."""
import os
import sys

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
if SCRIPT_PATH not in sys.path:
    sys.path.insert(0, SCRIPT_PATH)

import export_all

if __name__ == "__main__":
    export_all.run()
