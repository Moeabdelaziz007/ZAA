"""Expose ``plugin_example`` under the ``sss`` namespace."""

from importlib import import_module

_module = import_module("plugin_example")
globals().update(
    {k: getattr(_module, k) for k in dir(_module) if not k.startswith("_")}
)
__file__ = _module.__file__
