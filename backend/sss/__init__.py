"""Compatibility package exposing core modules under the 'sss' namespace."""
from importlib import import_module

zero_system = import_module("zero_system")
plugin_example = import_module("plugin_example")

__all__ = ["zero_system", "plugin_example"]
