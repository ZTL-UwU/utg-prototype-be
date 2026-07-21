## tests for the PATCH /levels/{id} endpoint

from apps.game.models import LevelType
from apps.game.schemas import LevelOut, LevelWriteIn
from apps.game.test.helpers import assert_matches_schema, patch


def _payload(**overrides):
    data = LevelWriteIn(
        title="Edited",
        level_type=LevelType.EDUCATION_LETTER_GRID,
        level_props={"letters": ["x"]},
        splash_background_asset_path="edited-bg.png",
        show_mascot_on_splash=True,
        is_published=False,
    ).model_dump()
    return {**data, **overrides}


### /levels/{id}  (update_level)

def test_update_level_success(client, seed):
    level = seed.level_ed1_letter_grid
    resp = patch(client, f"/api/levels/{level.id}", _payload(), seed.auth_headers)
    assert resp.status_code == 200
    assert_matches_schema(resp.json(), LevelOut)
    level.refresh_from_db()
    assert level.title == "Edited"
    assert level.splash_background_asset_path == "edited-bg.png"
    assert level.updated_by_id == seed.user.id


def test_update_level_requires_auth(client, seed):
    resp = patch(client, f"/api/levels/{seed.level_ed1_letter_grid.id}", _payload())
    assert resp.status_code == 401


def test_update_level_not_found(client, seed):
    resp = patch(client, "/api/levels/999999", _payload(), seed.auth_headers)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Level not found."}


def test_update_level_unknown_level_type(client, seed):
    payload = _payload(level_type="nope")
    resp = patch(client, f"/api/levels/{seed.level_ed1_letter_grid.id}", payload, seed.auth_headers)
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Unknown level type."}


def test_update_level_mascot_not_found(client, seed):
    payload = _payload(mascot_id=999999)
    resp = patch(client, f"/api/levels/{seed.level_ed1_letter_grid.id}", payload, seed.auth_headers)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Mascot not found."}
