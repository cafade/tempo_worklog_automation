from pathlib import Path
from typing import Any, Dict

import yaml


def load_yaml_file(yaml_file_path: Path) -> Dict[str, Any]:
    """
    Loads YAML file.

    :param yaml_file_path: absoulte path to YAML file.
    :return: python object with loaded YAML file.
    """
    with open(yaml_file_path, "r") as yaml_file:
        return yaml.safe_load(yaml_file)
