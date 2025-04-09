import sys
sys.path.append('.')
import unittest
from pyGitHubAPI.github_api import ghAPI

class TestGitAPI(unittest.TestCase) : 
    
    def test_get_octocat(self) : 
        res = ghAPI.get_octocat()
        self.assertIsNotNone(res)
        self.assertEqual(res.status_code, 200)
        # print(res.headers)
        # print(res.text)

    def test_get_repository_README(self) : 
        owner = 'sindresorhus'
        repo = 'awesome'

        res = ghAPI.get_repository_README(owner, repo)
        self.assertIsNotNone(res)
        self.assertEqual(res.status_code, 200)
        # print(res.headers)
        # print(res.text)

    def test_get_search_repositories(self) : 
        q = 'deep learning in:readme'
        
        res = ghAPI.get_search_repositories(q)
        self.assertIsNotNone(res)
        self.assertEqual(res.status_code, 200)
        # print(res.headers)
        # print(res.text)

        next_url = res.links['next']['url']
        if next_url : 
            res = ghAPI.get_req(next_url)
            self.assertIsNotNone(res)
            self.assertEqual(res.status_code, 200)
            # print(res.headers)
            # print(res.text)

    def test_get_repository_content(self) : 
        owner = 'vinta'
        repo = 'awesome-python'
        path = 'requirements.txt'
        res = ghAPI.get_repository_content(owner, repo, path)
        self.assertEqual(res.status_code, 200)
        print(res.text)

    def test_get_list_repository_issues(self) : 
        owner = 'vinta'
        repo = 'awesome-python'

        res = ghAPI.get_list_repository_issues(owner, repo)
        self.assertEqual(res.status_code, 200)
        print(res.text)

    def test_get_list_pull_requests(self) : 
        owner = 'vinta'
        repo = 'awesome-python'

        res = ghAPI.get_list_pull_requests(owner, repo)
        self.assertEqual(res.status_code, 200)
        print(res.text)

    def test_get_repository(self) : 
        owner = 'vinta'
        repo = 'awesome-python'

        res = ghAPI.get_repository(owner, repo)
        self.assertEqual(res.status_code, 200)
        print(res.text)

    def test_get_issue_event(self) : 
        owner = 'Redocly'
        repo = 'redoc'
        number = 2002

        res = ghAPI.get_issue_events(owner, repo, number)
        self.assertEqual(res.status_code, 200)
        print(res.text)

if __name__ == '__main__' : 
    unittest.main()
    