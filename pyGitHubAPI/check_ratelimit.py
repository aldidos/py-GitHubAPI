import sys
sys.path.append('.')
import os
from github_api import ghAPI
from util import compute_rate_limit_time_seconds

res = ghAPI.get_rate_limit()
remaining = res.headers.get('x-ratelimit-remaining')
print(f'rate remaining = {remaining}')

reset_time_sec = compute_rate_limit_time_seconds(res)
reset_time_min = reset_time_sec / 60
print( f'reset time (min) = {reset_time_min}' )



