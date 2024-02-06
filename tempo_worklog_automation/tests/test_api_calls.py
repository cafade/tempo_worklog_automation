import pytest

from tempo_worklog_automation.client import make_async_api_requests
from tempo_worklog_automation.client.models import WorklogModel
from tempo_worklog_automation.settings import settings


@pytest.mark.skipif(
    not settings.run_integration_tests,
    reason="Integration tests are disabled by default.",
)
def test_load_issue_model(load_csv_file_with_valid_values) -> None:  # type: ignore # noqa: E501
    """
    Test load_issue_model function.

    GIVEN a csv file path string
    WHEN load_csv_file is called
    THEN object with contents of csv file must be returned
    """
    csv_object = load_csv_file_with_valid_values

    list_of_worklogs = [
        WorklogModel(
            issue=worklog["issue"],
            time_spent=worklog["time_spent"],
            start_date=worklog["start_date"],
            start_time=worklog["start_time"],
        )
        for worklog in csv_object["worklogs"]
    ]

    responses = make_async_api_requests(list_of_worklogs)  # type: ignore

    for response in responses:  # type: ignore
        assert response == 200
