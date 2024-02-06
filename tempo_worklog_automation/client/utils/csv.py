import csv
from pathlib import Path
from typing import Any, Dict, List


def load_csv_file(csv_file_path: Path) -> Dict[str, Any]:
    DictionaryData = Dict[str, List[Any]]
    dictionary_data: DictionaryData = {"worklogs": []}

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
