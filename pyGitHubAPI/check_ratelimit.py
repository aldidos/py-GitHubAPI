import sys
sys.path.append('.')
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller
from pyGitHubAPI.config import make_headers
from util import compute_rate_limit_time_seconds
from requests import Session

session = Session()

def get_ratelimits(token) : 
    print(f'TOKEN : {token}')   

    headers = make_headers(token)
    session.headers.update( headers )
    res = GhAPISessionCaller.get_rate_limit(session)

    remaining = res.headers.get('x-ratelimit-remaining') 
    print(f'rate remaining = {remaining}')

    reset_time_sec = compute_rate_limit_time_seconds(res)
    reset_time_min = reset_time_sec / 60
    print( f'reset time (min) = {reset_time_min}' )

if __name__ == '__main__' : 
    p_tokens = sys.argv[1:]
    for p_token in p_tokens : 
        get_ratelimits(p_token)
        print()