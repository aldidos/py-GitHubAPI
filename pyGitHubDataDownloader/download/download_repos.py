import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader, DataFileWriter
from pyGitHubAPI.async_gh_api_caller import AsyncGHApiCaller
from pyGitHubDataDownloader.github_mass_scraper import GitHubMassScraper
from pyGitHubDataDownloader.response_callbacks import write_response_json
import asyncio

async def download_repositories(dataset, output_dir, gh_tokens) : 
    args = [ 
         (
            [ row['name'] ],  ## api args.
            [f'{output_dir}/{order}.json'], ## res args.
            order
         )
         for order, row in enumerate(dataset) ]  

    scraper = GitHubMassScraper(gh_tokens)
    await scraper.run(
        args, 
        AsyncGHApiCaller.get_repositories,
        write_response_json
        )
     
if __name__ == '__main__' :     
    in_args = DataFileReader.from_json( sys.argv[1] ) 
    input_file_path = in_args['in_file_path']
    output_dir = in_args['output_dir_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 
    dataset = DataFileReader.from_json(input_file_path)

    asyncio.run(download_repositories(dataset, output_dir, gh_tokens))