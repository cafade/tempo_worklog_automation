from tempo_worklog_automation.client import make_async_create_worklog_requests
from tempo_worklog_automation.client.models import WorklogModel
from tempo_worklog_automation.client.utils.arguments import parse_args
from tempo_worklog_automation.client.utils.csv import load_csv_file
from tempo_worklog_automation.client.utils.log import LoggingClass
from tempo_worklog_automation.settings import settings


# TODO: use these as reference if needed: https://github.com/awiddersheim/tempocli -
#  https://github.com/szymonkozak/tempomat
#  TODO: try implementing async post requests with:
#  https://www.python-httpx.org/async/#anyio
def main() -> None:
    """Main function."""
    logger_instance = LoggingClass(
        name=settings.logger_name,
        level=settings.log_level.value,
    )
    logger = logger_instance.create_logger()

    logger.info("Uploading worklogs.")

    cli_arguments = parse_args()

    csv_object = load_csv_file(cli_arguments.file_path)

    list_of_worklogs = [
        WorklogModel(
            issue=worklog["issue"],
            time_spent=worklog["time_spent"],
            start_date=worklog["start_date"],
            start_time=worklog["start_time"],
        )
        for worklog in csv_object["worklogs"]
    ]

    make_async_create_worklog_requests(list_of_worklogs)  # type: ignore

    logger.info("Finished upload.")


if __name__ == "__main__":
    main()
    # test comment
