"""Expose the core zero_system module under the ``sss`` namespace."""

from importlib import import_module

_module = import_module("zero_system")

# Re-export all public attributes from the real module
globals().update(
    {k: getattr(_module, k) for k in dir(_module) if not k.startswith("_")}
)

# Ensure file path points to the original module so log files are stored beside it
__file__ = _module.__file__
