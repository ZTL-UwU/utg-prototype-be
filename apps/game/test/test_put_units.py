## tests for every PUT (reorder) endpoint for /units

from apps.game.test.helpers import put


### /units/{unit_id}/levels/order  (reorder_levels)

def test_reorder_levels_success(client, seed):
    desert, sandstorm = seed.level_typing_desert, seed.level_typing_sandstorm
    resp = put(
        client,
        f"/api/units/{seed.unit_typing.id}/levels/order",
        {"level_ids": [sandstorm.id, desert.id]},  # reverse
        seed.auth_headers,
    )
    assert resp.status_code == 200
    # Response is the unit with levels re-sequenced
    assert [lvl["id"] for lvl in resp.json()["levels"]] == [sandstorm.id, desert.id]
    # New order persisted to the DB
    desert.refresh_from_db()
    sandstorm.refresh_from_db()
    assert (sandstorm.sort_order, desert.sort_order) == (1, 2)


def test_reorder_levels_requires_auth(client, seed):
    desert, sandstorm = seed.level_typing_desert, seed.level_typing_sandstorm
    resp = put(
        client,
        f"/api/units/{seed.unit_typing.id}/levels/order",
        {"level_ids": [sandstorm.id, desert.id]},
    )  # no auth headers
    assert resp.status_code == 401 # auth error code
    # Ordering untouched
    desert.refresh_from_db()
    assert desert.sort_order == 1


def test_reorder_levels_unit_not_found(client, seed):
    resp = put(client, "/api/units/999999/levels/order", {"level_ids": []}, seed.auth_headers)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Unit not found."}


def test_reorder_levels_incomplete_set(client, seed):
    # missing sandstorm causes set mismatch
    resp = put(
        client,
        f"/api/units/{seed.unit_typing.id}/levels/order",
        {"level_ids": [seed.level_typing_desert.id]},
        seed.auth_headers,
    )
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Level order must include each unit level exactly once."}


def test_reorder_levels_duplicate_ids(client, seed):
    desert = seed.level_typing_desert
    resp = put(
        client,
        f"/api/units/{seed.unit_typing.id}/levels/order",
        {"level_ids": [desert.id, desert.id]},
        seed.auth_headers,
    )
    assert resp.status_code == 400


def test_reorder_levels_foreign_id(client, seed):
    # A level belonging to a different unit is not part of this unit's set
    resp = put(
        client,
        f"/api/units/{seed.unit_typing.id}/levels/order",
        {"level_ids": [seed.level_typing_desert.id, seed.level_ed1_letter_grid.id]},
        seed.auth_headers,
    )
    assert resp.status_code == 400


### /units/list-by-layer/{layer}/order  (reorder_units)

def test_reorder_units_success(client, seed):
    ed_1, ed_2 = seed.unit_ed_1, seed.unit_ed_2
    resp = put(
        client,
        "/api/units/list-by-layer/education/order",
        {"unit_ids": [ed_2.id, ed_1.id]},  # reverse
        seed.auth_headers,
    )
    assert resp.status_code == 200
    # Response is the layer's units re-sequenced
    assert [u["id"] for u in resp.json()] == [ed_2.id, ed_1.id]
    ed_1.refresh_from_db()
    ed_2.refresh_from_db()
    assert (ed_2.sort_order, ed_1.sort_order) == (1, 2)


def test_reorder_units_requires_auth(client, seed):
    resp = put(
        client,
        "/api/units/list-by-layer/education/order",
        {"unit_ids": [seed.unit_ed_2.id, seed.unit_ed_1.id]},
    )  # no auth headers
    assert resp.status_code == 401


def test_reorder_units_incomplete_set(client, seed):
    # Missing unit_ed_2 -> set mismatch
    resp = put(
        client,
        "/api/units/list-by-layer/education/order",
        {"unit_ids": [seed.unit_ed_1.id]},
        seed.auth_headers,
    )
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Unit order must include each layer unit exactly once."}


def test_reorder_units_duplicate_ids(client, seed):
    ed_1 = seed.unit_ed_1
    resp = put(
        client,
        "/api/units/list-by-layer/education/order",
        {"unit_ids": [ed_1.id, ed_1.id]},
        seed.auth_headers,
    )
    assert resp.status_code == 400
