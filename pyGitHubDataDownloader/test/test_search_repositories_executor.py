import sys
sys.path.append('.')
from pyGitHubDataDownloader.executor.search_repositories_executor import SearchRepositoriesExecutor
import json

def test_get_repositories() : 
    q = 'open-source in:readme'

    srh = SearchRepositoriesExecutor(q)
    result = srh.get_repositories()

    print( result )
    file_path = './test_get_repositories_result.json'
    with open(file_path, mode='w', encoding='utf-8') as f :
        json.dump(result, f)

test_get_repositories()