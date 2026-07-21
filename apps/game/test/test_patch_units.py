## tests for the PATCH /units/{id} endpoint

from apps.game.schemas import UnitByIdOut, UnitUpdateIn
from apps.game.test.helpers import assert_matches_schema, patch


def _payload(**overrides):
    data = UnitUpdateIn(
        layer="typing",
        title="Renamed",
        title_font_size=30,
        background_asset_path="new.png",
        is_published=False,
    ).model_dump()
    return {**data, **overrides}


### /units/{id}  (update_unit)

def test_update_unit_success(client, seed, admin, admin_headers):
    resp = patch(client, f"/api/units/{seed.unit_ed_1.id}", _payload(), admin_headers)
    assert resp.status_code == 200
    assert_matches_schema(resp.json(), UnitByIdOut)
    seed.unit_ed_1.refresh_from_db()
    assert seed.unit_ed_1.title == "Renamed"
    assert seed.unit_ed_1.layer == "typing"
    assert seed.unit_ed_1.updated_by_id == admin.id


def test_update_unit_forbidden(client, seed):
    # regular user lacks game.change_unit
    original = seed.unit_ed_1.title
    resp = patch(client, f"/api/units/{seed.unit_ed_1.id}", _payload(), seed.auth_headers)
    assert resp.status_code == 403
    assert resp.json() == {"detail": "You do not have permissions to edit units"}
    seed.unit_ed_1.refresh_from_db()
    assert seed.unit_ed_1.title == original


def test_update_unit_requires_auth(client, seed):
    resp = patch(client, f"/api/units/{seed.unit_ed_1.id}", _payload())
    assert resp.status_code == 401


def test_update_unit_not_found(client, admin_headers):
    resp = patch(client, "/api/units/999999", _payload(), admin_headers)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Unit not found."}


def test_update_unit_invalid_layer(client, seed, admin_headers):
    resp = patch(client, f"/api/units/{seed.unit_ed_1.id}", _payload(layer="bogus"), admin_headers)
    assert resp.status_code == 422
