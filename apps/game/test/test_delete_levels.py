## tests for the DELETE /levels/{id} endpoint

from apps.game.models import Level


### /levels/{id}  (delete_level)

def test_delete_level_success(client, seed):
    level_id = seed.level_ed1_letter_grid.id
    resp = client.delete(f"/api/levels/{level_id}", **seed.auth_headers)
    assert resp.status_code == 204
    assert not Level.objects.filter(id=level_id).exists()


def test_delete_level_requires_auth(client, seed):
    level_id = seed.level_ed1_letter_grid.id
    resp = client.delete(f"/api/levels/{level_id}")
    assert resp.status_code == 401
    assert Level.objects.filter(id=level_id).exists()


def test_delete_level_not_found(client, seed):
    resp = client.delete("/api/levels/999999", **seed.auth_headers)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Level not found."}
