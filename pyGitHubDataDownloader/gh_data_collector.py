from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.util import delay
from pathlib import Path
import json

class GHDataCollector : 

    def get_repository(self, owner, repo, output_dir) :         
        res = ghAPI.get_repository(owner, repo) 
        if res.status_code == 200 : 
            res_body = res.text
            repository = json.loads(res_body)
            repo_id = repository['id']       
            Path(f'{output_dir}/{repo_id}.json').write_text(res_body, encoding ='utf-8')
            print(f'{repo_id} downloaded')

    def get_pull_request_review_comments_list(self, repo_id, owner, name, page, output_base_path) :     
        output_path = Path(f'{output_base_path}/{repo_id}')
        output_path.mkdir(exist_ok = True)

        try : 
            res = ghAPI.get_list_review_comments(owner, repo=name, per_page = 100, page = page)        
            status_code = res.status_code
            if status_code == 200 : 
                output_file_path = f'{output_path}/{page}.json'
                Path(output_file_path).write_text(res.text, encoding = 'utf-8')
                page += 1
            else : 
                print(f'ERROR : {repo_id}\t{res.status_code}')            
        except : 
            print(f'EXCEPTION : {repo_id}')

    def get_pull_request_review(self, repo_id, pull_request_url, pull_request_review_id, output_base_path) : 
        output_path = Path(f'{output_base_path}/{repo_id}')
        output_path.mkdir(exist_ok = True)
        
        url = f'{pull_request_url}/reviews/{pull_request_review_id}'

        print(url)

        try : 
            res = ghAPI.get_rate_limit()
            delay(res)
            
            res = ghAPI.get_req(url)        
            if res.status_code == 200 : 
                output_file_path = f'{output_path}/{pull_request_review_id}.json'
                Path(output_file_path).write_text(res.text, encoding = 'utf-8')
            else : 
                print(f'ERROR : {repo_id}\t{res.status_code}')            
        except : 
            print(f'EXCEPTION : {repo_id}')

    def get_list_pull_requests(self, owner, repo, state, page, output_base_path) : 
        output_path = Path(f'{output_base_path}/{repo}') 
        output_path.mkdir(exist_ok = True)    

        try : 
            res = ghAPI.get_list_pull_requests(owner, repo, state, page = page)            
            if res.status_code == 200 : 
                output_file_path = f'{output_path}/{page}.json'
                Path(output_file_path).write_text(res.text, encoding = 'utf-8')
                print(f'get {output_file_path}')
        except Exception as e:         
            print(f'{e}')

ghDataCollector = GHDataCollector()