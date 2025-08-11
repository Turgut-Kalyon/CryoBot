"""
Author: Turgut Kalyon
Description: FileOperations module for CryoBot, providing methods to load and write YAML files.
"""
import os
from abc import abstractmethod
import yaml

CURRENT_DIR = os.getcwd()


class FileOperations:

    def __init__(self, file_path):
        self.file_path = CURRENT_DIR + file_path

    def load_file(self):
        with open(self.file_path, 'r', encoding="utf-8") as file:
            return yaml.safe_load(file)

    @abstractmethod
    def write_file(self, data):
        pass


class CustomCommandsFileOperations(FileOperations):

    def __init__(self, file_path):
        super().__init__(file_path)

    def write_file(self, data):
        with open(self.file_path, 'w', encoding="utf-8") as file:
            yaml.dump({"commands": data}, file, allow_unicode=True)
