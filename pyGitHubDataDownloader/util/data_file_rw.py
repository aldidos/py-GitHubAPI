import json
import csv
from pathlib import Path

class DataFileReader : 

    def from_json(file_path) : 
        with open(file_path, mode = 'r', encoding = 'utf-8') as f : 
            return json.load(f)

    def from_csv(file_path) : 
        with open(file_path, mode = 'r', encoding = 'utf-8-sig') as f : 
            reader = csv.DictReader(f)
            return [ row for row in reader ]

    def find_files(path, extension) : 
        return Path(path).glob(f'**/*.{extension}')     
        
class DataFileWriter : 

    def to_json(file_path, dataset : list, default = None) :         
        with open(file_path, mode = 'w', encoding = 'utf-8') as wf : 
            if default == None : 
                json.dump(dataset, wf)
            else : 
                json.dump(dataset, wf, default = default)

    def to_csv(file_path, fieldnames : list[str],  dataset : list) : 
        with open(file_path, mode = 'w', encoding = 'utf-8') as wf : 
            writer = csv.DictWriter(wf, fieldnames = fieldnames, lineterminator = '\n')
            writer.writeheader()
            writer.writerows(dataset)