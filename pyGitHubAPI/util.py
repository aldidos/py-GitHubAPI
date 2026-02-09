import json
import datetime
import time

def write_text_to_json(path : str, text : str) : 
    with open(path, mode='w', encoding='utf-8') as f : 
        json.dump( json.loads(text), f )

def delay(res, n_remaining = 100) : 
    remaining = res.headers.get('x-ratelimit-remaining')
    remaining = int(remaining)
    if remaining <= n_remaining : 
        wait_second = compute_rate_limit_time_seconds(res)
        wait_second = wait_second + 60
        if wait_second < 0 : 
            wait_second = 60
        print(f'wait for {wait_second} seconds.')
        time.sleep(wait_second) 

def compute_rate_limit_time_seconds(res) : 
    ratelimit_reset = res.headers.get('x-ratelimit-reset')
    ratelimit_reset_value = int(ratelimit_reset)
    ratelimit_time = datetime.datetime.fromtimestamp( ratelimit_reset_value )
    diff_time = ratelimit_time - datetime.datetime.today()
    return diff_time.total_seconds()