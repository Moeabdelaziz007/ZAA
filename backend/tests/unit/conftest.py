import os
import sys

  # Ensure the project root is on sys.path so tests can import the package
  <<<<<<< codex/resolve-merge-conflicts-and-update-tests
  ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
  =======
  ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
  >>>>>>> main
  if ROOT_DIR not in sys.path:
      sys.path.insert(0, ROOT_DIR)
