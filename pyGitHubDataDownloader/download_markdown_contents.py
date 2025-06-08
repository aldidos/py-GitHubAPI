import sys
sys.path.append('.')
import csv
from pyGitHubDataDownloader.gh_content_explorer import GHContentExplorer

def explorer_pull_request_template_markdown_file(repo_owner, repo_name) : 
    contents = []
    
    result = GHContentExplorer.find_content_with(repo_owner, repo_name, '', '.md')
    contents.extend( result )

    result = GHContentExplorer.find_content_with(repo_owner, repo_name, '.github', '.md')
    contents.extend( result )

    result = GHContentExplorer.find_content_with(repo_owner, repo_name, '.github/PULL_REQUEST_TEMPLATE', '.md') ####
    contents.extend( result )

    return contents

output_file = open('./repo_markdown_contents.txt', mode = 'w', encoding = 'utf-8')

if __name__ == '__main__' : 

    input_file_path = './temp.csv'

    with open(input_file_path, mode = 'r', encoding = 'utf-8-sig') as f : 
        reader = csv.DictReader(f)
        
        for row in reader :             
            repo_id = row['repo_id']
            repo_owner = row['repo_owner']
            repo_name = row['repo_name']

        contents = explorer_pull_request_template_markdown_file(repo_owner, repo_name)

        for content in contents : 
            name = content['name']
            path = content['path']
            download_url = content['download_url']

            output_str = f'{repo_id}\t{repo_owner}\t{repo_name}\t{name}\t{path}\t{download_url}\n'
            output_file.write( output_str )

        print(repo_id)
    
    output_file.close()