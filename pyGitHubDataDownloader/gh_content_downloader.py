from pyGitHubAPI.github_api import ghAPI, delay
from pathlib import Path

class GHContentDownloader : 

    def __init__(self, download_base_path, log_file_path) : 
        self.log_file = open(log_file_path, mode = 'w', encoding = 'utf-8')
        self.download_base_path = Path(download_base_path)

    def close(self) : 
        self.log_file.close()

    def log_message(self, message) : 
        self.log_file.write(message)

    def download(self, repo_id, repo_owner, repo_name, file_name, file_path, download_url) : 
        res = ghAPI.get_req(download_url)
        if res.status_code == 200 : 
            output_path = self.download_base_path / f'{repo_id}'

            temp_file_path = Path(file_path)
            for i in range(len( temp_file_path.parts ) - 1) : 
                output_path /= temp_file_path.parts[i]

            output_path.mkdir(parents = True, exist_ok = True) 
            output_path = output_path / file_name
            output_path.write_text(res.text, encoding = 'utf-8') 
            log_mes = f'{repo_id}\t{repo_owner}\t{repo_name}\t{file_name}\t{file_path}\tSUCCESS\n'
            self.log_message(log_mes)
            print(log_mes)
        else : 
            log_mes = f'{repo_id}\t{repo_owner}\t{repo_name}\t{file_name}\t{file_path}\tFAILED_DOWNLOAD_REQUEST\n'
            self.log_message(log_mes)
            print(log_mes)
        
        delay(res)