import importlib
import pytest
from src.types import AgedBrie


def _find_AgedBrie():
    """Try a few likely module paths and return the AgedBrie class or skip."""
    candidates = [
        "gildedrose.domain.aged_brie",
        "gildedrose.aged_brie",
        "aged_brie",
        "domain.aged_brie",
    ]
    for mod in candidates:
        try:
            module = importlib.import_module(mod)
        except ImportError:
            continue
        if hasattr(module, "AgedBrie"):
            return module.AgedBrie
    pytest.skip("AgedBrie not found in known locations", allow_module_level=True)


def _get(obj, *names):
    """Return first existing attribute or method value from names."""
    for n in names:
        if hasattr(obj, n):
            v = getattr(obj, n)
            return v() if callable(v) else v
    raise AttributeError(f"None of {names} found on {obj}")


def _call_update(obj):
    for name in ("update_quality", "updateQuality", "update"):
        if hasattr(obj, name):
            fn = getattr(obj, name)
            if callable(fn):
                return fn()
    raise AttributeError("No update method found on object")


def test_create_aged_brie():
    cheese = AgedBrie("Aged Brie", 2, 0)
    name = _get(cheese, "name", "get_name", "getName")
    sell_in = _get(cheese, "sell_in", "get_sell_in", "getSell_in")
    quality = _get(cheese, "quality", "get_quality", "getQuality")

    assert name == "Aged Brie"
    assert sell_in == 2
    assert quality == 0


def test_str_representation():
    assert isinstance(str(AgedBrie("Aged Brie", 2, 0)), str)


def test_update_quality_brie():
    cheese = AgedBrie("Aged Brie", 2, 0)
    _call_update(cheese)

    assert _get(cheese, "sell_in", "get_sell_in", "getSell_in") == 1
    assert _get(cheese, "quality", "get_quality", "getQuality") == 1


def test_update_quality_brie_expired():
    cheese = AgedBrie("Aged Brie", 0, 0)
    _call_update(cheese)

    assert _get(cheese, "sell_in", "get_sell_in", "getSell_in") == -1
    assert _get(cheese, "quality", "get_quality", "getQuality") == 2


@pytest.mark.parametrize("start_quality, expected", [(50, 50), (49, 50)])
def test_quality_max_50(start_quality, expected):
    brie = AgedBrie("Aged Brie", -1, start_quality)
    _call_update(brie)

    assert _get(brie, "sell_in", "get_sell_in", "getSell_in") == -2
    assert _get(brie, "quality", "get_quality", "getQuality") == expected
