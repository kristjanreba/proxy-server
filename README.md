# Python HTTP Proxy Server

This is a simple Python HTTP proxy server that appends a JSON Web Token (JWT) to POST requests. The JWT contains specific claims like iat (Timestamp of the request), jti (Cryptographic nonce), and payload (A JSON payload containing user information and date).

The proxy server is built to sign the JWT using the HS512 algorithm and a secret key defined in the script. The signed JWT is then added as the x-my-jwt header to the upstream POST request.

The upstream post endpoint can be any dummy endpoint for testing purposes.


### Setup
```shell
make build
make up
```

### Access
```
URL: localhost:8081/status
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
