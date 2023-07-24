# Python Task

### Setup
```shell
make up
```

### Access
```
URL: localhost:8080/status
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

