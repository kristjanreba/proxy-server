import json

import jwt
import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from proxy_server import generate_jwt, proxy_handler, status_handler


def test_generate_jwt():
    secret_key = (
        b"a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4"  # noqa
    )
    test_payload = {"user": "testuser", "date": "2023-07-24"}

    # Generate JWT for the test payload
    jwt_token = generate_jwt(test_payload)

    # Assertion: Ensure the generated JWT is not None and is a string
    assert jwt_token is not None
    assert isinstance(jwt_token, str)
    assert len(jwt_token) > 0

    # Assertion: Verify specific claims in the generated JWT
    decoded_jwt = jwt.decode(jwt_token, secret_key, algorithms=["HS512"])
    assert decoded_jwt["user"] == test_payload["user"]
    assert decoded_jwt["date"] == test_payload["date"]

    # Assertion: Verify the signature validity of the JWT
    try:
        jwt.decode(
            jwt_token, secret_key, algorithms=["HS256"]
        )  # Use incorrect algorithm to raise an exception
        assert False, "Invalid signature verification should raise an exception"
    except jwt.InvalidSignatureError:
        pass  # Exception is expected as the algorithm used for verification is incorrect

    # Assertion: Ensure the payload is not tampered with
    altered_payload = {"user": "hacker", "date": "2023-07-24"}
    altered_jwt = generate_jwt(altered_payload)
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(altered_jwt, secret_key, algorithms=["HS512"])


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

    print(response.status)
    print(response)

    # The response should have status code 201 (created) from the upstream endpoint
    assert response.status == 201

    # The response should have the 'x-my-jwt' header
    assert "x-my-jwt" in response.headers


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
