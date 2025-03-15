import sys
sys.path.append('.')
from pyGitHubAPI.handler.search_repositories_handler import SearchRepositoriesHandler

def test_get_repositories() : 
    q = 'deep learning in:readme'

    srh = SearchRepositoriesHandler(q)
    result = srh.get_repositories()

    print( result )

test_get_repositories()