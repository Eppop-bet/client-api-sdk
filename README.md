# Esource.gg Python SDK

This is a Python SDK for interacting with the Esource.gg REST API.  
It provides a simple, consistent interface for authentication and accessing resources such as sports and maps.

## Features

- Authenticated session management
- Reusable base resource class with built-in filtering support (`skip`, `limit`, `orderBy`, `search`)
- Modular design for easy extension
- Integration tested against the live API

## Installation

Clone the repository and install in editable mode:

```bash
pip install -e .
```

## Usage
```
from client_api import Session, Sports

session = Session(
    base_url="https://esource.gg/api",
    email="sdk@test.com",
    password="yourpassword"
)

sports = Sports(session)
results = sports.list_sports(limit=10, order_by="name")
print(results)
```
