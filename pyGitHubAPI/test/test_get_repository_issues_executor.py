import sys
sys.path.append('.')
from pyGitHubAPI.handler.get_repository_issues_executor import GetRepositoryIssuesExecutor
from pyGitHubAPI.pagenator import pagenator

def test_execute() : 
    owner = 'sindresorhus'
    repo = 'awesome'

    executor = GetRepositoryIssuesExecutor(owner, repo, state='closed')
    res = executor.execute()

    print( len(executor.result) )
    print(executor.result)

def test_get_next_items() : 
    owner = 'sindresorhus'
    repo = 'awesome'

    executor = GetRepositoryIssuesExecutor(owner, repo, state='closed')
    res = executor.execute()

    executor.get_next_items(res)

    print( len(executor.result) )
    print(executor.result)

test_execute()
test_get_next_items()