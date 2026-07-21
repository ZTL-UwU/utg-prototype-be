## shared test helpers for the game api

import json


def assert_matches_schema(item: dict, schema):
    # validate types/required fields against the schema and pin the exact key set
    schema.model_validate(item)
    assert item.keys() == schema.model_fields.keys()


def _json_request(method, client, url, payload, headers):
    return method(url, data=json.dumps(payload), content_type="application/json", **(headers or {}))


def post(client, url, payload, headers=None):
    return _json_request(client.post, client, url, payload, headers)


def put(client, url, payload, headers=None):
    return _json_request(client.put, client, url, payload, headers)


def patch(client, url, payload, headers=None):
    return _json_request(client.patch, client, url, payload, headers)
