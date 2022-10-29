from aiohttplimiter import RateLimitExceeded, Limiter, default_keyfunc
from aiohttp.web import Request, View
from utils import create_json_response



def get_user_ip(request: Request or View) -> str:
    '''
    Returns the user's IP
    '''
    assert isinstance(request, Request or View)
    
    ip = request.remote or '127.0.0.1'
    ip = ip.split(",")[0]
    return ip


def rate_limit_err_handler(request: Request, exc: RateLimitExceeded):
    '''
    handle rate limit messages
    '''
    return create_json_response(
        data={
            "msg": "Woah!! Slow down a bit",
            "rate_limit": exc.detail,
        },
        status_code=429
    )



limiter = Limiter(
    keyfunc=get_user_ip,
    # exempt_ips={"127.0.0.1"},
    error_handler=rate_limit_err_handler
)