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
NormalItem = getattr(mod, "NormalItem", None)
if NormalItem is None:
    pytest.skip("NormalItem not available in types module", allow_module_level=True)


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


def test_crear_normal_item():
    normal = NormalItem("+5 Dexterity Vest", 10, 20)
    assert _get(normal, "name", "get_name", "getName") == "+5 Dexterity Vest"
    assert _get(normal, "sell_in", "get_sell_in", "get_sell_in") == 10
    assert _get(normal, "quality", "get_quality", "getQuality") == 20


def test_to_string():
    normal = NormalItem("+5 Dexterity Vest", 10, 20)
    assert isinstance(str(normal), str)


def test_update_quality_normal_item():
    normal = NormalItem("+5 Dexterity Vest", 10, 20)
    _call(normal, "updateQuality", "update_quality")
    assert _get(normal, "sell_in", "get_sell_in", "get_sell_in") == 9
    assert _get(normal, "quality", "get_quality", "getQuality") == 19


def test_update_quality_normal_item_expired():
    normal = NormalItem("+5 Dexterity Vest", 0, 20)
    _call(normal, "updateQuality", "update_quality")
    assert _get(normal, "sell_in", "get_sell_in", "get_sell_in") == -1
    assert _get(normal, "quality", "get_quality", "getQuality") == 18


def test_quality_min_zero():
    normal = NormalItem("+5 Dexterity Vest", 10, 0)
    _call(normal, "updateQuality", "update_quality")
    assert _get(normal, "sell_in", "get_sell_in", "get_sell_in") == 9
    assert _get(normal, "quality", "get_quality", "getQuality") == 0
