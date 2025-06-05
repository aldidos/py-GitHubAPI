import time
import re
from pyGitHubAPI.github_api import ghAPI
import json
from pathlib import Path

def is_pull_request_template(file_name : str) : 
    str = file_name.lower()
    mat = re.match('pull_request_template.md', str)
    if mat : 
        return True
    return False

class PRTDownloader : 

    def __init__(self, download_base_path, log_file_path) : 
        self.log_file = open(log_file_path, mode = 'w', encoding = 'utf-8')
        self.download_base_path = Path(download_base_path)

    def close(self) : 
        self.log_file.close()

    def log_message(self, message) : 
        self.log_file.write(message)

    def delay(self, res) : 
        remaining = res.headers.get('x-ratelimit-remaining')
        remaining = int(remaining)
        if remaining == 0 : 
            wait_second = ghAPI.compute_rate_limit_time_seconds(res)
            print(f'wait for {wait_second} seconds.')
            time.sleep(wait_second)            

    def download_pull_request_template(self, repo_id, repo_owner, repo_name, path) : 
        res = ghAPI.get_repository_content(repo_owner, repo_name, path)
        status_code = res.status_code
        if status_code == 200 : 
            b_state = False
            files = json.loads( res.text )
            for file in files : 
                if is_pull_request_template(file['name']) : 
                    download_url = file['download_url']
                    b_state = True
                    temp_res = ghAPI.get_req(download_url)
                    if temp_res.status_code == 200 : 
                        output_path = self.download_base_path / f'{repo_id}'
                        output_path.mkdir(exist_ok = True) 
                        output_path = output_path / file['name']
                        output_path.write_text(temp_res.text, encoding = 'utf-8') 
                        self.log_message(f'{repo_id}\t{repo_owner}\t{repo_name}\t{path}\tSUCCESS\n')
                        print(f'{repo_id}\t{repo_owner}\t{repo_name}\t{path}\tSUCCESS')
                    else : 
                        self.log_message(f'{repo_id}\t{repo_owner}\t{repo_name}\t{path}\tFAILED_DOWNLOAD_REQUEST\n')
                        print(f'{repo_id}\t{repo_owner}\t{repo_name}\t{path}\tFAILED_DOWNLOAD_REQUEST')
                    break
            if b_state == False : 
                self.log_message(f'{repo_id}\t{repo_owner}\t{repo_name}\t{path}\tFAILED_FILE_NOT_FOUND\n')
                print(f'{repo_id}\t{repo_owner}\t{repo_name}\t{path}\tFAILED_FILE_NOT_FOUND')
        else : 
            self.log_message(f'{repo_id}\t{repo_owner}\t{repo_name}\t{path}\tFAILED_GET_CONTENT_REQUEST\n')
            print(f'{repo_id}\t{repo_owner}\t{repo_name}\t{path}\tFAILED_GET_CONTENT_REQUEST')
        
        self.delay(res)