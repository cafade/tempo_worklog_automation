import argparse

from tempo_worklog_automation.client.models import CliArguments


def parse_args() -> CliArguments:
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
    cli_arguments = CliArguments(file_path=unvalidated_file_path)

    return cli_arguments
