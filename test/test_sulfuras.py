import importlib
import pytest
from typing import Any


def _load_types_module():
    for name in ("src.types", "types", "gildedrose.domain.types", "gildedrose.types"):
        try:
            return importlib.import_module(name)
        except ImportError:
            continue
    pytest.skip("types module not found (expected src.types)", allow_module_level=True)


mod = _load_types_module()
Sulfuras = getattr(mod, "Sulfuras", None)
if Sulfuras is None:
    pytest.skip("Sulfuras not available in types module", allow_module_level=True)


def _get(obj: Any, *names):
    for n in names:
        if hasattr(obj, n):
            val = getattr(obj, n)
            return val() if callable(val) else val
    raise AttributeError(f"None of the names {names} found on object {obj}")


def _call(obj: Any, *names, call_args=(), call_kwargs=None):
    """Call the first existing method named in *names on obj.

    Optional `call_args` (tuple) and `call_kwargs` (dict) are forwarded.
    """
    if call_kwargs is None:
        call_kwargs = {}
    for n in names:
        if hasattr(obj, n):
            fn = getattr(obj, n)
            if callable(fn):
                return fn(*call_args, **call_kwargs)
    raise AttributeError(f"None of the methods {names} found on object {obj}")


def test_crear_sulfuras():
    s = Sulfuras("Sulfuras, Hand of Ragnaros", 0, 80)
    assert _get(s, "name", "get_name", "getName") == "Sulfuras, Hand of Ragnaros"
    assert _get(s, "sell_in", "get_sell_in", "getSell_in") == 0
    assert _get(s, "quality", "get_quality", "getQuality") == 80


def test_to_string():
    s = Sulfuras("Sulfuras, Hand of Ragnaros", 0, 80)
    assert isinstance(str(s), str)


def test_update_quality_sulfuras():
    s = Sulfuras("Sulfuras, Hand of Ragnaros", 0, 80)
    _call(s, "updateQuality", "update_quality")
    assert _get(s, "sell_in", "get_sell_in", "getSell_in") == 0
    assert _get(s, "quality", "get_quality", "getQuality") == 80
