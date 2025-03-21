import sys
sys.path.append('.')
from pyGitHubAPI.handler.search_repositories_handler import SearchRepositoriesHandler
import json

def test_get_repositories() : 
    q = 'open-source in:readme'

    srh = SearchRepositoriesHandler(q)
    result = srh.get_repositories()

    print( result )
    file_path = './test_get_repositories_result.json'
    with open(file_path, mode='w', encoding='utf-8') as f :
        json.dump(result, f)

test_get_repositories()