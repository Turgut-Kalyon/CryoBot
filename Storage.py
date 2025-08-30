import os
import yaml
current_dir = os.getcwd()

class Storage:
    def __init__(self, main_key, source):
        self.source = source
        self.main_key = main_key
        self.yaml_file = self.load_yaml_file()

    def save(self) -> None:
        with open(self.source, 'w', encoding="utf-8") as file:
            yaml.dump(self.yaml_file, file, allow_unicode=True)

    def _fetch_file_content(self) -> dict:
        if not os.path.exists(self.source):
            return {}
        try:
            with open(self.source, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            print(f"Error reading {self.source}: {e}")
            return {}

    def load_yaml_file(self) -> dict:
        data = self._fetch_file_content()
        data.setdefault(self.main_key, {})
        return data

    def delete(self, key) -> None:
        if self.exists(key):
            del self.yaml_file[self.main_key][key]
            self.save()

    def clear(self) -> None:
        self.yaml_file = {f"{self.main_key}": {}}
        self.save()

    def exists(self, key) -> bool:
        return key in self.yaml_file[self.main_key]

    def get(self, key) -> dict:
        return self.yaml_file[self.main_key].get(key, None)

    def set(self, key, value) -> None:
        self.yaml_file[self.main_key][key] = value
        self.save()

    def adjust(self, key: str, delta: int) -> None:
        if self.exists(key):
            current_value = self.yaml_file[self.main_key][key]
            new_value = max(0, current_value + delta)
            self.yaml_file[self.main_key][key] = new_value
            self.save()

    def set_all(self, value) -> None:
        keys = self.yaml_file[self.main_key].keys()
        self.yaml_file[self.main_key] = dict.fromkeys(keys, value)
        self.save()
