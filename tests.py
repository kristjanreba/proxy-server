import json

import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from proxy_server import proxy_handler, status_handler


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
