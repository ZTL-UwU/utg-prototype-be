## tests for the GET /mascots endpoint

from apps.game.schemas import MascotOut
from apps.game.test.helpers import assert_matches_schema


### /mascots/list

def test_list_mascots(client, seed):
    resp = client.get("/api/mascots/list")
    assert resp.status_code == 200
    data = resp.json()
    for mascot in data:
        assert_matches_schema(mascot, MascotOut)
    # ordered by (name, id): "Camel" sorts before "sheep"
    assert [m["id"] for m in data] == [seed.mascot_camel.id, seed.mascot_sheep.id]
