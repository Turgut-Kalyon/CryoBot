import os
import yaml
CURRENT_DIR = os.getcwd()



class FileOperations:
    def __init__(self, file_path):
        self.file_path = CURRENT_DIR + file_path

    def load_file(self):
        with open(self.file_path, 'r') as file:
            return yaml.safe_load(file)

    def write_file(self, data):
        with open(self.file_path, 'a') as file:
            yaml.dump(data, file)




