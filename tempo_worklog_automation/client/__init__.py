from typing import Any, Dict, List, Union

import anyio
import httpx

from tempo_worklog_automation.client.models import WorklogModel
from tempo_worklog_automation.settings import settings


async def get_issue_id(issue_name: str) -> int:
    jira_account_email = settings.jira_account_email
    jira_token = settings.jira_token

    url = f"{settings.jira_base_api_url}/{issue_name}"
    auth = (jira_account_email, jira_token)
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=headers, auth=auth)

    return response.json()["id"]


async def parse_worklog(
    worklog: WorklogModel,
    author_account_id: str,
) -> Dict[str, Any]:
    issue_id = await get_issue_id(worklog.issue)
    parsed_worklog = {
        "authorAccountId": author_account_id,
        "description": worklog.issue,
        "issueId": issue_id,
        "startDate": worklog.start_date,
        "startTime": worklog.start_time,
        "timeSpentSeconds": worklog.time_spent,
    }

    return parsed_worklog


async def run_api_requests(
    list_of_worklogs: List[WorklogModel],
) -> Union[List[httpx.Response], List[int]]:
    """
    Run api post requests from list of WorklogsModels, run through anyio backend asyncio.

    :param value: validation string.
    :raises ValueError: when validator condition fails.
    :return: validation string.
    """

    tempo_oauth_token = settings.tempo_oauth_token
    author_account_id = settings.author_account_id

    url = settings.tempo_base_api_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tempo_oauth_token}",
    }
    responses = []
    for worklog in list_of_worklogs:
        parsed_worklog = await parse_worklog(worklog, author_account_id)

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url=url,
                    headers=headers,
                    json=parsed_worklog,
                )
                responses.append(response)
                response.raise_for_status()

            except httpx.HTTPStatusError as exc:
                decoded_content = exc.response.content.decode("utf-8")
                print(
                    f"Error response {exc.response.status_code!r} while requesting {exc.request.url!r}.\n\t{decoded_content}",
                )
                raise
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")
                raise

    return [response.status_code for response in responses]


def make_async_api_requests(list_of_worklogs: List[WorklogModel]) -> None:
    """
    Run api post requests from list of WorklogsModels, run through anyio backend asyncio.

    :param value: validation string.
    :raises ValueError: when validator condition fails.
    :return: validation string.
    """
    return anyio.run(run_api_requests, list_of_worklogs, backend="asyncio")  # type: ignore
