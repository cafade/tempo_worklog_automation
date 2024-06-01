import csv
from pathlib import Path
from typing import Any, Dict, List


def load_csv_file(csv_file_path: Path) -> Dict[str, Any]:
    """
    Load parsed csv file then return as dictionary.

    :param csv_file_path: Path object for the csv file.
    :return: dictionary_data with parsed csv file.
    """
    dictionary_data_init = Dict[str, List[Any]]
    dictionary_data: dictionary_data_init = {"worklogs": []}

    with open(
        csv_file_path,
        mode="r",
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            worklog = {
                "issue": row["issue"],
                "time_spent": row["time_spent"],
                "start_date": row["start_date"],
                "start_time": row["start_time"],
            }

            dictionary_data["worklogs"].append(worklog)

    return dictionary_data
