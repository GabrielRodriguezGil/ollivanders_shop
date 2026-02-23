import importlib
import pytest


def _find_Conjured():
    candidates = [
        "gildedrose.domain.conjured",
        "gildedrose.conjured",
        "conjured",
        "domain.conjured",
    ]
    for mod in candidates:
        try:
            module = importlib.import_module(mod)
        except ImportError:
            continue
        if hasattr(module, "Conjured"):
            return module.Conjured
    pytest.skip("Conjured not found in known locations", allow_module_level=True)


Conjured = _find_Conjured()


def _get(obj, *names):
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


def test_create_conjured():
    c = Conjured("Conjured Mana Cake", 3, 6)
    assert _get(c, "name", "get_name", "getName") == "Conjured Mana Cake"
    assert _get(c, "sell_in", "get_sell_in", "getSell_in") == 3
    assert _get(c, "quality", "get_quality", "getQuality") == 6


def test_str_representation():
    assert isinstance(str(Conjured("Conjured Mana Cake", 3, 6)), str)


def test_update_quality_conjured():
    c = Conjured("Conjured Mana Cake", 3, 6)
    _call_update(c)
    assert _get(c, "sell_in", "get_sell_in", "getSell_in") == 2
    assert _get(c, "quality", "get_quality", "getQuality") == 4


def test_update_quality_conjured_just_expired():
    c = Conjured("Conjured Mana Cake", 0, 6)
    _call_update(c)
    assert _get(c, "sell_in", "get_sell_in", "getSell_in") == -1
    assert _get(c, "quality", "get_quality", "getQuality") == 2


def test_update_quality_conjured_expired():
    c = Conjured("Conjured Mana Cake", -1, 6)
    _call_update(c)
    assert _get(c, "sell_in", "get_sell_in", "getSell_in") == -2
    assert _get(c, "quality", "get_quality", "getQuality") == 2


def test_quality_min_zero():
    c = Conjured("Conjured Mana Cake", 1, 1)
    _call_update(c)
    assert _get(c, "sell_in", "get_sell_in", "getSell_in") == 0
    assert _get(c, "quality", "get_quality", "getQuality") == 0

    c = Conjured("Conjured Mana Cake", -1, 0)
    _call_update(c)
    assert _get(c, "sell_in", "get_sell_in", "getSell_in") == -2
    assert _get(c, "quality", "get_quality", "getQuality") == 0
