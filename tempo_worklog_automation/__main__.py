from tempo_worklog_automation.client import make_async_api_requests
from tempo_worklog_automation.client.models import WorklogModel
from tempo_worklog_automation.client.utils.arguments import parse_args
from tempo_worklog_automation.client.utils.csv import load_csv_file


# TODO: use these as reference if needed: https://github.com/awiddersheim/tempocli -
#  https://github.com/szymonkozak/tempomat
#  TODO: try implementing async post requests with:
#  https://www.python-httpx.org/async/#anyio
def main() -> None:
    """Main function."""

    print("Uploading worklogs.")  # noqa: WPS421

    # project_root = dirname(__file__)
    # load_csv_file_path = Path(f"{project_root}/tests/resources/valid_worklogs.csv")
    # csv_object = load_csv_file(load_csv_file_path)

    cli_arguments = parse_args()
    file_path = cli_arguments.file_path

    csv_object = load_csv_file(file_path)

    list_of_worklogs = [
        WorklogModel(
            issue=worklog["issue"],
            time_spent=worklog["time_spent"],
            start_date=worklog["start_date"],
            start_time=worklog["start_time"],
        )
        for worklog in csv_object["worklogs"]
    ]

    make_async_api_requests(list_of_worklogs)  # type: ignore

    print("Finished upload.")  # noqa: WPS421


if __name__ == "__main__":
    main()
