import pytest


@pytest.mark.anyio
async def test_load_yaml(load_yaml_file_with_random_values) -> None:  # type: ignore
    """
    Test load_yaml_file function.

    GIVEN a yaml file path string
    WHEN yaml.safe_load is called
    THEN object with contents of yaml file must be returned
    """
    yaml_object = load_yaml_file_with_random_values

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
