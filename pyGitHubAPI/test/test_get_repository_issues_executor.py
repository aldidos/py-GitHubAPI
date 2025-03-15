import sys
sys.path.append('.')
from pyGitHubAPI.handler.get_repository_issues_executor import GetRepositoryIssuesExecutor

def test_execute() : 
    owner = 'sindresorhus'
    repo = 'awesome'

    executor = GetRepositoryIssuesExecutor(owner, repo, state='closed')
    result = executor.execute()

    print( len(result) )
    print(result)

test_execute()
