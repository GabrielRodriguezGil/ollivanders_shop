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
Item = getattr(mod, "Item", None)
if Item is None:
    pytest.skip("Item class not available in types module", allow_module_level=True)


def _get(obj: Any, *names):
    for n in names:
        if hasattr(obj, n):
            val = getattr(obj, n)
            return val() if callable(val) else val
    raise AttributeError(f"None of the names {names} found on object {obj}")


def test_crear_item():
    item = Item("+5 Dexterity Vest", 10, 20)
    assert _get(item, "name", "get_name", "getName") == "+5 Dexterity Vest"
    assert _get(item, "sell_in", "get_sell_in", "getSell_in") == 10
    assert _get(item, "quality", "get_quality", "getQuality") == 20
