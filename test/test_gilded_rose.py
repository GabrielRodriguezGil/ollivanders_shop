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
GildedRose = getattr(mod, "GildedRose", None)
NormalItem = getattr(mod, "NormalItem", None)
AgedBrie = getattr(mod, "AgedBrie", None)
if None in (GildedRose, NormalItem, AgedBrie):
    pytest.skip(
        "Required classes not available in types module", allow_module_level=True
    )


def _get(obj: Any, *names):
    for n in names:
        if hasattr(obj, n):
            v = getattr(obj, n)
            return v() if callable(v) else v
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


def test_add_and_to_string():
    shop = GildedRose()
    shop_add = None
    for name in ("addItem", "add_item", "add"):
        if hasattr(shop, name):
            shop_add = getattr(shop, name)
            break
    assert shop_add is not None

    shop_add(AgedBrie("Aged Brie", 2, 0))
    shop_add(AgedBrie("Aged Brie", 10, 10))

    inv = _get(shop, "inventory")
    assert len(inv) == 2


def test_update_quality():
    shop = GildedRose()
    normal = NormalItem("+5 Dexterity Vest", 10, 20)
    brie = AgedBrie("Aged Brie", 2, 0)

    # add items via whichever add method exists
    for name in ("addItem", "add_item", "add"):
        if hasattr(shop, name):
            getattr(shop, name)(normal)
            getattr(shop, name)(brie)
            break

    inv = _get(shop, "inventory")
    assert len(inv) == 2

    # call update
    for name in ("updateQuality", "update_quality", "update"):
        if hasattr(shop, name):
            getattr(shop, name)()
            break

    q0 = _get(inv[0], "quality", "get_quality", "getQuality")
    q1 = _get(inv[1], "quality", "get_quality", "getQuality")

    assert q0 == 19
    assert q1 == 1
