import sys
sys.path.append('.')
import unittest
from pyGitHubAPI.github_api import ghAPI
from pathlib import Path

class TestGitAPI(unittest.TestCase) : 
    
    def test_get_octocat(self) : 
        res = ghAPI.get_octocat()
        self.assertIsNotNone(res)
        self.assertEqual(res.status_code, 200)

    def test_get_repository_README(self) : 
        owner = 'sindresorhus'
        repo = 'awesome'

        res = ghAPI.get_repository_README(owner, repo)
        self.assertIsNotNone(res)
        self.assertEqual(res.status_code, 200)

    def test_get_search_repositories(self) : 
        q = 'deep learning in:readme'
        
        pagenator = ghAPI.get_search_repositories(q)
        res = pagenator.__next__()
        self.assertEqual(res.status_code, 200)         

    def test_get_repository_content(self) : 
        owner = 'vinta'
        repo = 'awesome-python'
        path = 'requirements.txt'
        res = ghAPI.get_repository_content(owner, repo, path)
        self.assertEqual(res.status_code, 200)        

    def test_get_list_repository_issues(self) : 
        owner = 'vinta'
        repo = 'awesome-python'

        pagenator = ghAPI.get_list_repository_issues(owner, repo)
        res = pagenator.__next__()
        self.assertEqual(res.status_code, 200)

    def test_get_list_pull_requests(self) : 
        owner = 'vinta'
        repo = 'awesome-python'

        pagenator = ghAPI.get_list_pull_requests(owner, repo)
        res = pagenator.__next__()
        self.assertEqual(res.status_code, 200)

    def test_get_repository(self) : 
        owner = 'vinta'
        repo = 'awesome-python'

        res = ghAPI.get_repository(owner, repo)
        self.assertEqual(res.status_code, 200)

    def test_get_issue_event(self) : 
        owner = 'Redocly'
        repo = 'redoc'
        number = 2002

        res = ghAPI.get_issue_events(owner, repo, number)
        self.assertEqual(res.status_code, 200)

    def test_get_list_commits(self) : 
        repo_id = 100057683
        owner = 'britecharts'
        repo = 'britecharts-react'
        path = '.github/PULL_REQUEST_TEMPLATE.md'

        output_path = Path(f'./repo_content/COMMITS/{repo_id}')
        output_path.mkdir(exist_ok = True)

        n_page = 1
        pagenator = ghAPI.get_list_commits(owner, repo, path)
        for res in pagenator : 
            self.assertEqual(res.status_code, 200)
            
            output_path = output_path / f'{n_page}.json'
            output_path.write_text(res.text, encoding = 'utf-8')
            n_page += 1

    def test_get_a_commit(self) : 
        owner = 'NicolasCARPi'
        repo = 'jquery_jeditable'
        ref = '3207325678af7af4bb397905b9697c1c106cd212'

        res = ghAPI.get_a_commit(owner, repo, ref)
        self.assertEqual(res.status_code, 200)
        print(res.text)


if __name__ == '__main__' : 
    unittest.main()
    