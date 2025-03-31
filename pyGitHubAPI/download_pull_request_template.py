import sys
sys.path.append('.')
from pyGitHubAPI.executor.repository_content_executor import RepositoryContentExecutor
from pathlib import Path
import csv

if __name__ == '__main__' :         
    input_file_path = sys.argv[1]
    output_path = sys.argv[2]

    executor = RepositoryContentExecutor()

    with open(input_file_path, mode = 'r', encoding = 'utf-8') as f : 
        reader = csv.DictReader(f)
        for row in reader : 
            id = row['id']
            owner = row['owner'] 
            name = row['name']
            content_paths = row['pull_request_template paths']
            print(f'Download pull-request-template of {id}')

            path = Path(f'{output_path}/{id}')
            if path.exists() :
               continue
            path.mkdir()

            paths = content_paths.split(';')
            num = 1
            
            for p in paths : 
                content = executor.download_repository_content(owner, name, p)
                download_file_path = f'{output_path}/{id}/{num}.md'
                with open(download_file_path, mode = 'w', encoding = 'utf-8') as f : 
                   f.write( content )
                num += 1