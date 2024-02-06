from os.path import dirname
from pathlib import Path
from typing import Any, Dict

import pytest

from tempo_worklog_automation.client.utils.csv import load_csv_file
from tempo_worklog_automation.client.utils.yaml import load_yaml_file


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
def load_yaml_file_with_random_values() -> Dict[str, Any]:
    """
    Loads YAML file.

    :return: python object with loaded YAML file.
    """
    project_root = dirname(__file__)
    load_yaml_file_path = Path(
        f"{project_root}/tests/resources/random_sample_worklogs.yaml",
    )
    return load_yaml_file(load_yaml_file_path)


@pytest.fixture(scope="session")
def load_yaml_file_with_valid_values() -> Dict[str, Any]:
    """
    Loads YAML file.

    :return: python object with loaded YAML file.
    """
    project_root = dirname(__file__)
    load_yaml_file_path = Path(f"{project_root}/tests/resources/valid_worklogs.yaml")
    return load_yaml_file(load_yaml_file_path)


@pytest.fixture(scope="session")
def load_csv_file_with_random_values() -> Dict[str, Any]:
    """
    Loads CSV file.

    :return: python object with loaded CSV file.
    """
    project_root = dirname(__file__)
    load_csv_file_path = Path(
        f"{project_root}/tests/resources/random_sample_worklogs.csv",
    )
    return load_csv_file(load_csv_file_path)


@pytest.fixture(scope="session")
def load_csv_file_with_valid_values() -> Dict[str, Any]:
    """
    Loads CSV file.

    :return: python object with loaded CSV file.
    """
    project_root = dirname(__file__)
    load_csv_file_path = Path(f"{project_root}/tests/resources/valid_worklogs.csv")
    return load_csv_file(load_csv_file_path)
