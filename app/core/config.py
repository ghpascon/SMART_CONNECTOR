import json
import os


class Settings:
    def __init__(self, config_path="config/config.json"):
        self.load()

    def load(self, config_path="config/config.json"):
        self._config_path = config_path
        self.data = {}
        self.data["STORAGE_DAYS"] = 1

        if os.path.exists(self._config_path):
            with open(self._config_path, "r") as f:
                self.data = json.load(f)

        if os.path.exists("config/actions.json"):
            with open("config/actions.json", "r") as f:
                actions_data = json.load(f)
                self.data["STORAGE_DAYS"] = actions_data.get("STORAGE_DAYS", 1)

    def save(self):
        with open(self._config_path, "w") as f:
            json.dump(self.data, f, indent=4)


settings = Settings()
