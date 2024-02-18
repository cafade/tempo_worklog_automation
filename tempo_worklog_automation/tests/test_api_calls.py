from datetime import datetime, timedelta

import pytest

from tempo_worklog_automation.client import (
    make_async_create_worklog_requests,
    make_async_delete_worklog_requests,
)
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

    # Get the current date
    current_date = datetime.today().date()

    # Calculate the weekday of the current date (0 is Monday,  6 is Sunday)
    current_weekday = current_date.weekday()

    # Calculate the date of the Monday of the current week
    monday_date = current_date - timedelta(days=current_weekday)

    # Format the Monday date in the "yyyy-mm-dd" format
    formatted_monday_date = monday_date.strftime("%Y-%m-%d")

    # Always load test worklogs in the current's week monday as weeks in the past are
    # closed for changes.
    list_of_worklogs = [
        WorklogModel(
            issue=worklog["issue"],
            time_spent=worklog["time_spent"],
            start_date=formatted_monday_date,
            start_time=worklog["start_time"],
        )
        for worklog in csv_object["worklogs"]
    ]

    try:
        results = make_async_create_worklog_requests(list_of_worklogs)  # type: ignore

        status_codes = results["status_codes"]  # type: ignore

        worklog_ids = results["worklog_ids"]  # type: ignore

        for status_code in status_codes:  # type: ignore
            assert status_code == 200
    finally:
        # pass
        results = make_async_delete_worklog_requests(worklog_ids)  # type: ignore

        for status_code in results:  # type: ignore
            assert status_code == 204
