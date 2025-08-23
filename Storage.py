import os
import yaml
current_dir = os.getcwd()

class Storage:
    def __init__(self, main_key, source):
        self.source = source
        self.main_key = main_key
        self.yaml_file = self.load_yaml_file()

    def save(self):
        with open(self.source, 'w', encoding="utf-8") as file:
            yaml.dump(self.yaml_file, file, allow_unicode=True)

    def fetch_file_content(self) -> dict:
        if not os.path.exists(self.source):
            return {}
        with open(self.source, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def load_yaml_file(self) -> dict:
        data = self.fetch_file_content()
        data.setdefault(self.main_key, {})
        return data

    def get_data(self, data):
        data.setdefault(self.main_key, {})
        return data

    def delete(self, key):
        if self.exists(key):
            del self.yaml_file[self.main_key][key]
            self.save()

    def clear(self):
        self.yaml_file = {f"{self.main_key}": {}}
        self.save()

    def exists(self, key):
        return key in self.yaml_file[self.main_key]

    def get(self, key):
        return self.yaml_file[self.main_key].get(key, None)

    def set(self, key, value):
        self.yaml_file[self.main_key][key] = value
        self.save()

    def adjust(self, key, value):
        if self.exists(key):
            new_value = max(0, self.yaml_file[self.main_key][key] + value)
            self.yaml_file[self.main_key][key] = new_value
            self.save()

    def set_all(self, value):
        keys = self.yaml_file[self.main_key].keys()
        self.yaml_file[self.main_key] = dict.fromkeys(keys, value)
        self.save()
