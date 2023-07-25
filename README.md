# Python HTTP Proxy Server

This is a simple Python HTTP proxy server that appends a JSON Web Token (JWT) to POST requests. The JWT contains specific claims like iat (Timestamp of the request), jti (Cryptographic nonce), and payload.

The proxy server is built to sign the JWT using the HS512 algorithm and a secret key defined in the script. The signed JWT is then added as the x-my-jwt header to the upstream POST request.

The upstream post endpoint can be any dummy endpoint for testing purposes but in our case we created a test server.


- The proxy server works asynchronously.
- We also provide test coverage of the functionality.
- You can check the up-time and number of requests of the proxy server on **/status** endpoint.


### Local environment setup
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run test server
python test_server.py

# run proxy server
python proxy_server.py

# run tests
pytest tests.py
```

### Setup with Docker
```shell
make build
make up

# to run tests
make test
```

### Access
```
# proxy service
POST localhost:8081
GET localhost:8081/status

# test server
POST localhost:8001
```

### Development setup
```shell
pip install pre-commit
pre-commit install

pip install -r requirements.txt
```
We use pre-commit to make sure the code is properly formatted.
When you make a commit it will automatically run multiple linters
and code formatting checks.

Running pre-commit helps keep code clean with each commit.
If you are in a hurry and can't make sure that the code is properly formatted,
use `git commit --no-verify -m "..."` to skip pre-commit checks.
