## tests for every GET endpoint for /units

import pytest

from apps.game.models import Unit
from apps.game.schemas import (
    LevelShortOut,
    MascotOut,
    SidebarUnitOut,
    UnitByIdOut,
    UnitByLayerOut,
    UnitOut,
)
from apps.game.test.helpers import assert_matches_schema


### /units/list

def test_list_units_returns_all_units_ordered(client, seed):
    # units ordered by (sort_order, id): typing(1,id1), ed_1(1,id2), ed_2(2,id3)
    resp = client.get("/api/units/list")
    assert resp.status_code == 200
    data = resp.json()
    for unit in data:
        assert_matches_schema(unit, UnitOut)
    assert [u["id"] for u in data] == [
        seed.unit_typing.id,
        seed.unit_ed_1.id,
        seed.unit_ed_2.id,
    ]


def test_list_units_nests_full_levels(client, seed):
    # UnitOut nests full LevelOut
    resp = client.get("/api/units/list")
    typing = next(u for u in resp.json() if u["id"] == seed.unit_typing.id)

    levels = typing["levels"]
    assert [lvl["sort_order"] for lvl in levels] == [1, 2]  # ordered by sort_order
    # mascot is a nested object (LevelOut), not just an id
    assert levels[0]["mascot"]["id"] == seed.mascot_camel.id
    assert_matches_schema(levels[0]["mascot"], MascotOut)


### /units/sidebar

def test_sidebar_units_shape_and_order(client, seed):
    # SidebarUnitOut is a slim schema: id/layer/title only, no levels/auditing
    resp = client.get("/api/units/sidebar")
    assert resp.status_code == 200
    data = resp.json()
    for unit in data:
        assert_matches_schema(unit, SidebarUnitOut)
    assert [u["id"] for u in data] == [
        seed.unit_typing.id,
        seed.unit_ed_1.id,
        seed.unit_ed_2.id,
    ]


### /units/list-by-layer/{layer}

def test_list_by_layer_education(client, seed):
    # Only education units, ordered by sort_order; typing unit excluded
    resp = client.get("/api/units/list-by-layer/education")
    assert resp.status_code == 200
    data = resp.json()
    for unit in data:
        assert_matches_schema(unit, UnitByLayerOut)
    assert [u["id"] for u in data] == [seed.unit_ed_1.id, seed.unit_ed_2.id]


def test_list_by_layer_typing(client, seed):
    resp = client.get("/api/units/list-by-layer/typing")
    assert resp.status_code == 200
    assert [u["id"] for u in resp.json()] == [seed.unit_typing.id]


def test_list_by_layer_uses_short_levels(client, seed):
    
    resp = client.get("/api/units/list-by-layer/education")
    ed_1 = next(u for u in resp.json() if u["id"] == seed.unit_ed_1.id)
    assert_matches_schema(ed_1["levels"][0], LevelShortOut)


def test_list_by_layer_empty(client, db):
    # No units seeded on the game layer
    resp = client.get("/api/units/list-by-layer/game")
    assert resp.status_code == 200
    assert resp.json() == []


### /units/{unit_id}

def test_get_unit_by_id(client, seed):
    resp = client.get(f"/api/units/{seed.unit_ed_1.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert_matches_schema(data, UnitByIdOut)
    assert data["id"] == seed.unit_ed_1.id
    assert data["title"] == seed.unit_ed_1.title
    assert data["layer"] == "education"
    assert [lvl["sort_order"] for lvl in data["levels"]] == [1, 2]  # sort_order


def test_get_unit_not_found_returns_404(client, seed):
    # Missing id
    resp = client.get("/api/units/999999")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Unit not found."}
