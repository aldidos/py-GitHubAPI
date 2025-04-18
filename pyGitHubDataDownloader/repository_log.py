
class RepositoryLog : 
    def __init__(self, file_path) : 
        self.repo_ids = set()

        try : 
            with open(file_path, mode = 'r') as f: 
                for l in f.readlines() : 
                    self.repo_ids.add( int(l) )
        except : 
            print('error the previous log file does not exist')

    def put(self, repo_id : int) : 
        self.repo_ids.add(repo_id)

    def has(self, repo_id : int) : 
        return repo_id in self.repo_ids

    def write_to_file(self, file_path) : 
        with open(file_path, mode = 'w', encoding = 'utf-8') as f : 
            for repo_id in self.repo_ids :                 
                f.write(str(repo_id))
                f.write('\n')
