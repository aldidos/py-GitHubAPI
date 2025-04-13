from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.pagenator import Pagenator
import json

class GetPRReviewExecutor : 

    def execute(self, owner, repo, pr_number) : 
        res = ghAPI.get_pull_request_reviews(owner, repo, pr_number)
        print(res.status_code)

        result = []

        if res.status_code == 200 : 
            data = json.loads(res.text)
            result.extend(data)

            pagenator = Pagenator(res)

            for res in pagenator : 
                print(res.status_code)
                if not res : 
                    data = json.loads(res.text)
                    result.extend(data) 

        return result
    
getPRReviewExecutor = GetPRReviewExecutor()