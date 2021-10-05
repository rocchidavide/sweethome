from pathlib import Path
import yaml


class Config:
    def __init__(self, yaml_files=None):
        self.configs = {}
        self.dots_dirs = {}
        if yaml_files:
            for filepath in yaml_files:
                self.add_config_from_yaml(filepath)

    def add_config_from_yaml(self, config_path):
        if not isinstance(config_path, Path):
            config_path = Path(config_path)
        with open(config_path, "r") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        self.configs[str(config_path)] = config
        for dot in config["installed_dots"]:
            # TODO: raise exception if dot already exists
            self.dots_dirs[dot] = config_path.parent

    @property
    def installed_dots(self):
        installed_dots = []
        for _, config in self.configs.items():
            installed_dots.extend(config["installed_dots"])
        return installed_dots

    def get_dot_path(self, dot_name):
        return self.dots_dirs.get(dot_name)


def get_config_from_yaml(config_file_path):
    config = {}
    with open(config_file_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config
