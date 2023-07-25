import json

import jwt
import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from proxy_server import generate_jwt, proxy_handler, status_handler


def test_generate_jwt():
    secret_key = b"a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf"  # noqa
    test_payload = {"user": "testuser", "date": "2023-07-24"}

    # Generate JWT for the test payload
    jwt_token = generate_jwt(test_payload)

    # Assertion: Ensure the generated JWT is not None and is a string
    assert jwt_token is not None
    assert isinstance(jwt_token, str)
    assert len(jwt_token) > 0

    # Verify specific claims in the generated JWT
    decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=["HS512"])
    assert decoded_jwt["payload"]["user"] == test_payload["user"]
    assert decoded_jwt["payload"]["date"] == test_payload["date"]

    # Verify the signature validity of the JWT
    with pytest.raises(jwt.exceptions.InvalidAlgorithmError):
        jwt.decode(
            jwt_token, secret_key, algorithms=["HS256"]
        )  # Use incorrect algorithm to raise an exception


@pytest_asyncio.fixture
@pytest.mark.asyncio
async def client():
    app = web.Application()
    app.router.add_route("POST", "/", proxy_handler)
    app.router.add_route("GET", "/status", status_handler)

    server = TestServer(app)
    client = TestClient(server)

    await client.start_server()
    yield client

    await client.close()
    await server.close()


@pytest.mark.asyncio
async def test_proxy_handler(client):
    # Test the POST request functionality
    payload = {
        "name": "morpheus",
        "job": "leader",
    }
    response = await client.post("/", data=json.dumps(payload))

    # The response should have status code 200 from the upstream endpoint
    assert response.status == 200


@pytest.mark.asyncio
async def test_status_handler(client):
    # Test the /status endpoint
    response = await client.get("/status")

    # The response should have status code 200 (OK)
    assert response.status == 200

    # The response should contain valid JSON data
    data = await response.json()
    assert "time_from_start" in data
    assert "request_count" in data
