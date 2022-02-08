# Testing codebase for issues
This assumes you have already followed `DEVELOPMENT.md`

## Install development lib
```bash
pip install -r requirements_dev.txt
```

## Running tests
### Linter
```bash
mypy src
```
### Linter 2
```bash
flake8 src
```
### Testing
```bash
pytest
```
