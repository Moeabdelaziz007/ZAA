  <<<<<<< codex/resolve-merge-conflicts-in-files
  """Test suite initialization."""
  import os
  import sys

  ROOT = os.path.dirname(os.path.dirname(__file__))
  if ROOT not in sys.path:
      sys.path.insert(0, ROOT)
  =======
  import os
  import sys

    <<<<<<< codex/remove-conflict-markers-and-refactor-tests
    ROOT = os.path.dirname(os.path.dirname(__file__))
    =======
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    >>>>>>> main
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
  >>>>>>> main
