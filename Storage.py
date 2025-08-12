import os
import yaml
current_dir = os.getcwd()

class Storage:
    def __init__(self, main_key, source=None):
        self.source = current_dir + source
        self.main_key = main_key
        self.yaml_file = self.load()

    def save(self, data: dict):
        with open(self.source, 'w', encoding="utf-8") as file:
            yaml.dump(data, file, allow_unicode=True)

    def load(self) -> dict:
        if not self.source or not os.path.isfile(self.source):
            return {self.main_key: {}}
        with open(self.source, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        return self.get_data(data)

    def get_data(self, data):
        return data if self.main_key in data else {self.main_key: {}}

    def delete(self, key):
        if key not in self.yaml_file[self.main_key]:
            return
        del self.yaml_file[self.main_key][key]
        self.save(self.yaml_file)

    def clear(self):
        data_to_write = {f"{self.main_key}": {}}
        self.yaml_file = data_to_write
        self.save(data_to_write)

    def exists(self, key) -> bool:
        return key in self.yaml_file[self.main_key]

    def get(self, key):
        return self.yaml_file[self.main_key].get(key, None)

    def set(self, key, value):
        self.yaml_file[self.main_key][key] = value
        self.save(self.yaml_file)

    def adjust(self, key, value):
        if not self.exists(key):
            return
        if self.is_result_getting_negative(key, value):
            self.set(key, 0)
            return
        value_before = self.yaml_file[self.main_key][key]
        self.set(key, value_before + value)


    def is_result_getting_negative(self, key, value):
        return self.yaml_file[self.main_key][key] + value <= 0

    def set_all(self, value):
        for key in self.yaml_file[self.main_key]:
            self.yaml_file[self.main_key][key] = value
        self.save(self.yaml_file)
