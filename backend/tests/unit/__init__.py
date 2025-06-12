  <<<<<<< codex/resolve-merge-conflicts-and-update-tests
  """Test suite initialization."""
  import os
  import sys

  ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
  =======
  """Unit test package initialization."""
  import os
  import sys

  ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
  >>>>>>> main
  if ROOT not in sys.path:
      sys.path.insert(0, ROOT)
