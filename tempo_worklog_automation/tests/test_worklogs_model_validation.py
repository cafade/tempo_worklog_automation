import pytest
from pydantic import ValidationError

from tempo_worklog_automation.client.models import WorklogModel


@pytest.mark.anyio
async def test_load_issue_model(load_csv_file_with_random_values) -> None:  # type: ignore # noqa: E501
    """
    Test load_issue_model function.

    GIVEN a csv file path string
    WHEN load_csv_file is called
    THEN object with contents of csv file must be returned

    :param load_csv_file_with_random_values: fixture to test csv files operations.
    """
    csv_object = load_csv_file_with_random_values

    worklog = csv_object["worklogs"][0]
    issue_model = WorklogModel(
        issue=worklog["issue"],
        time_spent=worklog["time_spent"],
        start_date=worklog["start_date"],
        start_time=worklog["start_time"],
    )
    assert issue_model.time_spent == 21600  # noqa: WPS432

    worklog = csv_object["worklogs"][1]
    issue_model = WorklogModel(
        issue=worklog["issue"],
        time_spent=worklog["time_spent"],
        start_date=worklog["start_date"],
        start_time=worklog["start_time"],
    )
    assert issue_model.time_spent == 19800  # noqa: WPS432

    worklog = csv_object["worklogs"][2]
    issue_model = WorklogModel(
        issue=worklog["issue"],
        time_spent=worklog["time_spent"],
        start_date=worklog["start_date"],
        start_time=worklog["start_time"],
    )
    assert issue_model.time_spent == 3

    worklog = csv_object["worklogs"][3]
    with pytest.raises(
        ValidationError,
        match='Time spent units must be in hours "h" or seconds "s"',
    ):
        WorklogModel(
            issue=worklog["issue"],
            time_spent=worklog["time_spent"],
            start_date=worklog["start_date"],
            start_time=worklog["start_time"],
        )
