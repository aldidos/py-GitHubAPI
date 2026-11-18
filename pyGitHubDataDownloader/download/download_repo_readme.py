import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pyGitHubAPI.async_gh_api_caller import AsyncGHApiCaller
from pyGitHubDataDownloader.github_mass_scraper import GitHubMassScraper
from pyGitHubDataDownloader.response_callbacks import write_response_json
import asyncio

async def download(dataset, output_dir, gh_tokens) :     
    args = [ 
        (
            [row['repo_name']],
            [ f'{output_dir}/{row["id"]}.json' ]
        )
            for row in dataset 
        ]    

    scraper = GitHubMassScraper(gh_tokens)
    await scraper.run(
        args, 
        AsyncGHApiCaller.get_repository_README, 
        write_response_json
        )
     
if __name__ == '__main__' :     
    in_args = DataFileReader.from_json( sys.argv[1] ) 
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 
    csv_data = DataFileReader.from_json( in_args['in_file_path'] )

    asyncio.run(download( csv_data, in_args['output_dir_path'], gh_tokens ))