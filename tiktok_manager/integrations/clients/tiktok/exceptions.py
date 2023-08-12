class TiktokClientError(Exception):
    pass


class TiktokClientProviderError(TiktokClientError):
    pass


class ResponseDataNotValidError(TiktokClientError):
    pass
