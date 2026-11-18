import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pyGitHubAPI.async_gh_api_caller import AsyncGHApiCaller
from pyGitHubDataDownloader.github_mass_scraper import GitHubMassScraper
from pyGitHubDataDownloader.response_callbacks import write_response_file_content
import asyncio

async def download_file_content_text(dataset, output_dir, gh_tokens) : 
    args = [ 
        (
            [ data['download_url'] ], 
            [ f"{output_dir}/{data['repo_id']}_{order}.json", data['repo_id'], data['file_name'], data['file_path'] ]
        )
        for order, data in enumerate(dataset)
    ]

    scraper = GitHubMassScraper(gh_tokens)
    await scraper.run(
        args, 
        AsyncGHApiCaller.get_url, 
        write_response_file_content
        )
    
if __name__ == '__main__' : 
    in_args = DataFileReader.from_json(sys.argv[1])    
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 
    dataset =  DataFileReader.from_json( in_args['input_file_path'] )

    asyncio.run( download_file_content_text(dataset, in_args['output_dir'], gh_tokens) ) 