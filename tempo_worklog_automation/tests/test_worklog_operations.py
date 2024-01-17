from os.path import dirname
from pathlib import Path

import pytest
from pydantic import ValidationError

from tempo_worklog_automation.src.models import IssueModel
from tempo_worklog_automation.src.utils.yaml import load_yaml_file


@pytest.mark.anyio
async def test_load_yaml() -> None:
    """
    Test load_yaml_file function.

    GIVEN a yaml file path string
    WHEN yaml.safe_load is called
    THEN object with contents of yaml file must be returned
    """
    project_root = dirname(dirname(__file__))
    load_yaml_file_path = Path(f"{project_root}/tests/resources/test_yaml_file.yaml")
    yaml_object = load_yaml_file(load_yaml_file_path)

    sample_dict = {
        "worklogs": [
            {
                "issue": "INT-10",
                "time_spent": "6h",
                "start_date": "2024-01-05",
                "start_time": "14:00:00",
            },
            {
                "issue": "INT-17",
                "time_spent": "5.5h",
                "start_date": "2024-01-23",
                "start_time": "13:00:00",
            },
            {
                "issue": "INT-15",
                "time_spent": "3s",
                "start_date": "2024-01-07",
                "start_time": "8:00:00",
            },
            {
                "issue": "INT-21",
                "time_spent": "4",
                "start_date": "2024-01-07",
                "start_time": "10:00:00",
            },
        ],
    }
    assert yaml_object == sample_dict


@pytest.mark.anyio
async def test_load_issue_model() -> None:
    """
    Test load_yaml_file function.

    GIVEN a yaml file path string
    WHEN yaml.safe_load is called
    THEN object with contents of yaml file must be returned
    """
    project_root = dirname(dirname(__file__))
    load_yaml_file_path = Path(f"{project_root}/tests/resources/test_yaml_file.yaml")
    yaml_object = load_yaml_file(load_yaml_file_path)

    worklog = yaml_object["worklogs"][0]
    issue_model = IssueModel(
        issue=worklog["issue"],
        time_spent=worklog["time_spent"],
        start_date=worklog["start_date"],
        start_time=worklog["start_time"],
    )
    assert issue_model.time_spent == 21600

    worklog = yaml_object["worklogs"][1]
    issue_model = IssueModel(
        issue=worklog["issue"],
        time_spent=worklog["time_spent"],
        start_date=worklog["start_date"],
        start_time=worklog["start_time"],
    )
    assert issue_model.time_spent == 19800

    worklog = yaml_object["worklogs"][2]
    issue_model = IssueModel(
        issue=worklog["issue"],
        time_spent=worklog["time_spent"],
        start_date=worklog["start_date"],
        start_time=worklog["start_time"],
    )
    assert issue_model.time_spent == 3

    worklog = yaml_object["worklogs"][3]
    with pytest.raises(
        ValidationError,
        match='Time spent units must be in hours "h" or seconds "s"',
    ):
        IssueModel(
            issue=worklog["issue"],
            time_spent=worklog["time_spent"],
            start_date=worklog["start_date"],
            start_time=worklog["start_time"],
        )
