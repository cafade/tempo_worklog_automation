import argparse

from tempo_worklog_automation.client.models import CliArguments


def parse_args() -> CliArguments:
    """
    Return CliArguments model with parsed cli args.

    :return: validation string.
    """
    parser = argparse.ArgumentParser(description="Worklogs file path.")

    parser.add_argument(
        "--file-path",
        default=None,
        required=True,
        help="Worklogs file path.",
        dest="file_path",
    )

    args = parser.parse_args()
    unvalidated_file_path = args.file_path

    return CliArguments(file_path=unvalidated_file_path)
