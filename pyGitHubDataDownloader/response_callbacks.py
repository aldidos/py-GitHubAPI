import os
from pyGitHubDataDownloader.util.data_file_rw import DataFileWriter
from pathlib import Path

async def default_response_callback(response) : 
    return await response.json()

async def write_response_json(response, output_file_path) : 
    data = await response.json()
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    DataFileWriter.to_json(output_file_path, data)

async def write_response_text(response, output_file_path) : 
    data = await response.text()
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    Path(output_file_path).write_text( data, 'utf-8' )    

async def write_response_file_content(response, output_file_path, repo_id, file_name, file_path) : 
    data = await response.text()
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    DataFileWriter.to_json(output_file_path, {
        'file_name' : file_name, 
        'file_path' : file_path, 
        'text' : data,
        'repo_id' : repo_id
    })    

async def extract_last_page_url(res, repo_id, repo_name) : 
    last_url = None        
    last = res.links.get('last')
    if last :             
        last_url = last['url']
    
    return {
        'repo_id' : repo_id,
        'repo_name' : repo_name, 
        'last_page_url' : str(last_url), 
        'response_status_code' : res.status
    } 