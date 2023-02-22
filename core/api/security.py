import os
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader, APIKeyQuery
from core.settings import environment_config

environment_config()
x_api_key_valid = os.environ.get('X-API-Key-Valid', None)
X_API_KEY_QUERY = APIKeyQuery(name="X-API-Key")
X_API_KEY_HEADER = APIKeyHeader(name="X-API-Key")


def check_api_key(
        api_key_query: str = Security(X_API_KEY_QUERY),
        api_key_header: str = Security(X_API_KEY_HEADER),
):
    if api_key_query == x_api_key_valid:
        return api_key_query
    elif api_key_header == x_api_key_valid:
        return api_key_header
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
        )
