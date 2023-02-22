import json

from typing import List, Any
from fastapi import FastAPI, Response, Depends
from fastapi.openapi.models import APIKey

from core.domain.api.patreon_response import PatreonModel

from fastapi_cache import FastAPICache, Coder
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from .security import check_api_key
from ..service.patreon_service import PatreonService

patreon_pledge_checker = FastAPI()
patreon_service = PatreonService(campaign_id=1874794)


class ResponseCoder(Coder):
    @classmethod
    def encode(cls, value: Any):
        return value

    @classmethod
    def decode(cls, value: Any):
        return value


@patreon_pledge_checker.get("/patreons", response_model=List[PatreonModel])
@cache(expire=180, coder=ResponseCoder)
async def get_patreons(api_key: APIKey = Depends(check_api_key)):
    all_patreons = patreon_service.get_all_patreon_members()

    dumps = json.dumps(all_patreons, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
    return Response(dumps, media_type="application/json")


@patreon_pledge_checker.get("/patreon", response_model=PatreonModel)
@cache(expire=180, coder=ResponseCoder)
async def get_patreons(patreon_uid: str, api_key: APIKey = Depends(check_api_key)):
    patreon = patreon_service.get_patreon(id_uid_patreon=patreon_uid)
    json_dumps = json.dumps(patreon, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
    return Response(json_dumps, media_type="application/json")


@patreon_pledge_checker.on_event("startup")
async def startup():
    backend = InMemoryBackend()
    FastAPICache.init(backend, prefix="in-memory-cache")
