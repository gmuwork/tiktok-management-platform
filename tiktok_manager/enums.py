import enum


class HttpMethod(enum.Enum):
    GET = "get"
    POST = "post"


class TimeIncrement(enum.Enum):
    DAY = 1
    WEEK = 7
    MONTH = 30


class ResourceType(enum.Enum):
    CAMPAIGN = "campaign"
    AD_GROUP = "adgroup"
    AD = "ad"
