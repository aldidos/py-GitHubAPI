import sys
sys.path.append('.')
from pyGitHubAPI.github_api import create_GitHubAPI
from util import compute_rate_limit_time_seconds

def get_ratelimits(token) : 
    print(f'TOKEN : {token}')

    ghAPI = create_GitHubAPI(token)
    res = ghAPI.get_rate_limit()
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