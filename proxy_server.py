import os
import aiohttp
import json
import time
import uuid
import hashlib
import hmac
import base64
from aiohttp import web

# Get the test server port from the TEST_SERVER_PORT environment variable
test_server_port = int(os.environ.get('TEST_SERVER_PORT', 8001))
proxy_port = int(os.environ.get('HTTP_PORT', 8080))

SECRET_KEY = b'a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf'  # noqa
UPSTREAM_URL = f'http://localhost:{test_server_port}'  # Replace this with your upstream endpoint

start_time = time.time()
request_count = 0


def generate_jwt(payload):
    header = {
        "alg": "HS512",
        "typ": "JWT"
    }

    claims = {
        "iat": int(time.time()),
        "jti": str(uuid.uuid4()),
        "payload": payload
    }

    encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b"=")
    encoded_claims = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=")

    signature = hmac.new(SECRET_KEY, encoded_header + b"." + encoded_claims, hashlib.sha512).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b"=")

    jwt = encoded_header + b"." + encoded_claims + b"." + encoded_signature

    return jwt.decode()


async def proxy_handler(request):
    global request_count
    content = await request.read()
    payload = json.loads(content.decode())
    jwt = generate_jwt(payload)

    headers = request.headers.copy()
    headers['x-my-jwt'] = jwt

    # Forward the modified request to the upstream endpoint using aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.post(UPSTREAM_URL, data=content, headers=headers) as response:
            # Increment the request count
            request_count += 1

            # Read the upstream response
            response_content = await response.read()

            return web.Response(body=response_content, status=response.status, headers=response.headers)


async def status_handler(request):
    global start_time, request_count

    # Calculate the time from start
    time_from_start = time.time() - start_time

    # Prepare the response JSON
    status_data = {
        "time_from_start": time_from_start,
        "request_count": request_count
    }

    return web.json_response(status_data)


def run_proxy_server():
    app = web.Application()
    app.router.add_route('POST', '/', proxy_handler)
    app.router.add_route('GET', '/status', status_handler)

    web.run_app(app, host='localhost', port=proxy_port)


if __name__ == '__main__':
    run_proxy_server()
