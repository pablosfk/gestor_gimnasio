import json
import os

class ThemeManager:
    @staticmethod
    def _get_config_path():
        app_data = os.getenv("APPDATA")
        base_path = os.path.join(app_data, "LearnLifting")
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        return os.path.join(base_path, "config.json")

    @classmethod
    def load_settings(cls):
        path = cls._get_config_path()
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except:
                pass
        # Defaults si no existe el archivo
        return {"mode": "dark", "color": "teal", "color_name": "Verde\nazulado"}

    @classmethod
    def save_settings(cls, mode, color, color_name):
        path = cls._get_config_path()
        settings = {"mode": mode, "color": color, "color_name": color_name}
        with open(path, "w") as f:
            json.dump(settings, f, indent=4)