"""Backend package initialization."""
import os
import sys

  <<<<<<< codex/resolve-merge-conflicts-and-update-tests
  ROOT = os.path.abspath(os.path.dirname(__file__))
  =======
  ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
  >>>>>>> main
  if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
