# Module 10: Secure User Model, Pydantic Validation, Database Testing, and Docker Deployment

## Overview
This application provides persistent relational storage using SQLAlchemy, request/response validation via Pydantic, password security via bcrypt hashing, and JWT token authentication.

## Running Tests Locally
Install requirements:
```bash
pip install -r requirements.txt
```

Execute unit and integration tests:
```bash
pytest -v
```

Execute integration tests with database state preserved:
```bash
pytest tests/test_integration.py -v -s --preserve-db
```

## Docker Hub Deployment
- **Docker Hub Repository:** https://hub.docker.com/r/ramiyamamataj/module10-auth
