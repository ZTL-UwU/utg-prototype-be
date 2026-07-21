## tests for the POST /units/{id}/levels endpoint

from apps.game.models import Level, LevelType
from apps.game.schemas import LevelOut, LevelWriteIn, MascotOut
from apps.game.test.helpers import assert_matches_schema, post


def _payload(**overrides):
    data = LevelWriteIn(
        level_type=LevelType.EDUCATION_LETTER_GRID,
        level_props={"letters": ["a", "b"]},
        splash_background_asset_path="bg.png",
        show_mascot_on_splash=False,
        is_published=True,
    ).model_dump()
    return {**data, **overrides}


### /units/{id}/levels  (create_level)

def test_create_level_success(client, seed):
    # unit_ed_2 already has one level (sort_order 1)
    resp = post(client, f"/api/units/{seed.unit_ed_2.id}/levels", _payload(), seed.auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert_matches_schema(body, LevelOut)
    assert body["sort_order"] == 2  # appended after existing level
    assert body["layer"] == "education"  # inherited from the unit
    assert body["created_by"] == seed.user.id
    assert Level.objects.filter(id=body["id"], unit_id=seed.unit_ed_2.id).exists()


def test_create_level_with_mascot(client, seed):
    payload = _payload(mascot_id=seed.mascot_sheep.id)
    resp = post(client, f"/api/units/{seed.unit_ed_1.id}/levels", payload, seed.auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["mascot"]["id"] == seed.mascot_sheep.id
    assert_matches_schema(body["mascot"], MascotOut)


def test_create_level_requires_auth(client, seed):
    resp = post(client, f"/api/units/{seed.unit_ed_1.id}/levels", _payload())
    assert resp.status_code == 401


def test_create_level_unit_not_found(client, seed):
    resp = post(client, "/api/units/999999/levels", _payload(), seed.auth_headers)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Unit not found."}


def test_create_level_unknown_level_type(client, seed):
    payload = _payload(level_type="nope")
    resp = post(client, f"/api/units/{seed.unit_ed_1.id}/levels", payload, seed.auth_headers)
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Unknown level type."}


def test_create_level_mascot_not_found(client, seed):
    payload = _payload(mascot_id=999999)
    resp = post(client, f"/api/units/{seed.unit_ed_1.id}/levels", payload, seed.auth_headers)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Mascot not found."}
