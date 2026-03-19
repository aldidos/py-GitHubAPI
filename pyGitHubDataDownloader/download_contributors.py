import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI, base_url, headers
from pyGitHubAPI.pagenator import Pagenator
from pyGitHubDataDownloader.gh_data_collector import ghDataCollector
import multiprocessing
from util.data_file_rw import DataFileReader
from pathlib import Path

def download(repo_id, owner, name) : 
    output_dir = sys.argv[2]
    url = f'{base_url}/repos/{owner}/{name}/contributors' 
    params = {
        'per_page' : 100, 
        'page' : 1,
        'anon' : True
    }
    print(url)

    output_path = f'{output_dir}/{repo_id}'
    Path(output_path).mkdir(exist_ok = True)

    n = 1
    pagenator = Pagenator(url, params, headers = headers)
    for res in pagenator : 
        if res.status_code == 200 :
            Path(f'{output_path}/{n}.json').write_text(res.text, encoding = 'utf-8')        
        n += 1   

if __name__ == '__main__' :     
    input_file_path = sys.argv[1] 
    
    dataset = []
    file_paths = DataFileReader.find_files(input_file_path, 'json')
    for file_path in file_paths : 
        repo_data = DataFileReader.from_json(file_path)
        repo_id = repo_data['id']
        name = repo_data['name']
        owner = repo_data['owner']['login']

        dataset.append( ( repo_id, owner, name ) )    
    
    with multiprocessing.Pool() as pool : 
        pool.starmap(download, dataset)