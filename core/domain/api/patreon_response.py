from enum import Enum

from pydantic import BaseModel


class Tier(str, Enum):
    TIER_1 = "Tier 1"
    TIER_2 = "Tier 2"
    TIER_3 = "Tier 3"


class Status(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class PatreonResponse:

    def __init__(self, user_id, patreon_uid, username='', status=Status.INACTIVE, mail="", tier=None):
        self.id = user_id
        self.patreon_uid = patreon_uid
        self.username = username
        self.mail = mail
        self.status = status
        self.tier = tier


class PatreonModel(BaseModel):
    user_id: str
    patreon_uid: str
    user_name: str
    mail: str
    status: Status
    tier: Tier
