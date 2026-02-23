import importlib
import pytest


def _find_Backstage():
    candidates = [
        "gildedrose.domain.backstage",
        "gildedrose.backstage",
        "backstage",
        "domain.backstage",
    ]
    for mod in candidates:
        try:
            module = importlib.import_module(mod)
        except ImportError:
            continue
        if hasattr(module, "Backstage"):
            return module.Backstage
    pytest.skip("Backstage not found in known locations", allow_module_level=True)


Backstage = _find_Backstage()


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


def test_create_backstage():
    pass_obj = Backstage("Backstage passes to a TAFKAL80ETC concert", 15, 20)
    assert (
        _get(pass_obj, "name", "get_name", "getName")
        == "Backstage passes to a TAFKAL80ETC concert"
    )
    assert _get(pass_obj, "sell_in", "get_sell_in", "getSell_in") == 15
    assert _get(pass_obj, "quality", "get_quality", "getQuality") == 20


def test_str_representation():
    assert isinstance(
        str(Backstage("Backstage passes to a TAFKAL80ETC concert", 15, 20)), str
    )


def test_update_quality_over_ten():
    p = Backstage("Backstage passes to a TAFKAL80ETC concert", 15, 20)
    _call_update(p)
    assert _get(p, "sell_in", "get_sell_in", "getSell_in") == 14
    assert _get(p, "quality", "get_quality", "getQuality") == 21


def test_update_quality_over_five():
    p = Backstage("Backstage passes to a TAFKAL80ETC concert", 6, 20)
    _call_update(p)
    assert _get(p, "sell_in", "get_sell_in", "getSell_in") == 5
    assert _get(p, "quality", "get_quality", "getQuality") == 22


def test_update_quality_over_zero():
    p = Backstage("Backstage passes to a TAFKAL80ETC concert", 5, 20)
    _call_update(p)
    assert _get(p, "sell_in", "get_sell_in", "getSell_in") == 4
    assert _get(p, "quality", "get_quality", "getQuality") == 23


def test_update_quality_pass_expired():
    p = Backstage("Backstage passes to a TAFKAL80ETC concert", 0, 20)
    _call_update(p)
    assert _get(p, "sell_in", "get_sell_in", "getSell_in") == -1
    assert _get(p, "quality", "get_quality", "getQuality") == 0


@pytest.mark.parametrize("start_sell, start_q", [(5, 49), (9, 49)])
def test_quality_max_50(start_sell, start_q):
    p = Backstage("Backstage passes to a TAFKAL80ETC concert", start_sell, start_q)
    _call_update(p)
    assert _get(p, "sell_in", "get_sell_in", "getSell_in") == start_sell - 1
    assert _get(p, "quality", "get_quality", "getQuality") == 50
