from os.path import dirname
from pathlib import Path

import pytest
from pydantic import ValidationError

from tempo_worklog_automation.src.models import IssueModel
from tempo_worklog_automation.src.utils.yaml import load_yaml_file


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

    sample_dict = {
        "worklogs": [
            {
                "issue": "INT-10",
                "time_spent": "1h",
                "start_date": "2024-01-05",
                "start_time": "14:00:00",
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

    worklog = sample_dict["worklogs"][0]
    IssueModel(
        issue=worklog["issue"],
        time_spent=worklog["time_spent"],
        start_date=worklog["start_date"],
        start_time=worklog["start_time"],
    )

    worklog = sample_dict["worklogs"][1]
    IssueModel(
        issue=worklog["issue"],
        time_spent=worklog["time_spent"],
        start_date=worklog["start_date"],
        start_time=worklog["start_time"],
    )

    worklog = sample_dict["worklogs"][2]
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
