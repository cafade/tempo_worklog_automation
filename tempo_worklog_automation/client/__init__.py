from typing import Any, Dict, List, Optional

import anyio
import httpx

from tempo_worklog_automation.client.models import WorklogModel
from tempo_worklog_automation.settings import settings


async def delete_worklog(
    responses: List[httpx.Response],
    worklog_id: int,
    client: httpx.AsyncClient,
    url: str,
    headers: Dict[str, str],
    max_retries: int = 5,
    backoff_factor: float = 0.5,
) -> Optional[httpx.Response]:
    for attempt in range(max_retries):
        try:
            response = await client.delete(
                url=f"{url}/{worklog_id}",
                headers=headers,
            )

            responses.append(response)
            response.raise_for_status()
            return response

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                wait_time = backoff_factor * (2**attempt)
                print(
                    f"Received HTTP  429 - Too Many Requests. Retrying in {wait_time} seconds...",
                )
                await anyio.sleep(wait_time)
            else:
                decoded_content = exc.response.content.decode("utf-8")
                print(
                    f"Error response {exc.response.status_code!r} while requesting {exc.request.url!r}.\n\t{decoded_content}",
                )
                raise
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
            raise

    print(f"All retries failed for {worklog_id}.")
    return None


async def run_delete_worklog_requests(
    worklog_ids: List[int],
) -> List[int]:
    tempo_oauth_token = settings.tempo_oauth_token

    url = settings.tempo_base_api_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tempo_oauth_token}",
    }
    responses: List[httpx.Response] = []
    async with httpx.AsyncClient() as client:
        async with anyio.create_task_group() as tg:
            for worklog_id in worklog_ids:
                tg.start_soon(
                    delete_worklog,
                    responses,
                    worklog_id,
                    client,
                    url,
                    headers,
                )

    return [response.status_code for response in responses]


def make_async_delete_worklog_requests(worklog_ids: List[int]) -> None:
    return anyio.run(run_delete_worklog_requests, worklog_ids, backend="asyncio")  # type: ignore


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


async def parse_and_create_worklog(
    responses: List[httpx.Response],
    worklog_ids: List[int],
    client: httpx.AsyncClient,
    worklog: WorklogModel,
    url: str,
    headers: Dict[str, str],
    author_account_id: str,
    max_retries: int = 5,
    backoff_factor: float = 0.5,
) -> Optional[httpx.Response]:
    parsed_worklog = await parse_worklog(worklog, author_account_id)

    for attempt in range(max_retries):
        try:
            response = await client.post(
                url=url,
                headers=headers,
                json=parsed_worklog,
            )
            responses.append(response)
            print(f"response.json(): {response.json()}")
            response.raise_for_status()
            worklog_ids.append(response.json()["tempoWorklogId"])
            return response

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                wait_time = backoff_factor * (2**attempt)
                print(
                    f"Received HTTP  429 - Too Many Requests. Retrying in {wait_time} seconds...",
                )
                await anyio.sleep(wait_time)
            else:
                decoded_content = exc.response.content.decode("utf-8")
                print(
                    f"Error response {exc.response.status_code!r} while requesting {exc.request.url!r}.\n\t{decoded_content}",
                )
                raise
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
            raise

    print(f"All retries failed for {parsed_worklog}.")
    return None


async def run_create_worklog_requests(
    list_of_worklogs: List[WorklogModel],
) -> Dict[str, Any]:
    """
    Run api post requests from list of WorklogsModels, run through anyio backend asyncio.

    :param value: validation string.
    :raises ValueError: when validator condition fails.
    :return: list of http response codes.
    """

    results: Dict[str, Any] = {"status_codes": [], "worklog_ids": []}

    tempo_oauth_token = settings.tempo_oauth_token
    author_account_id = settings.author_account_id

    url = settings.tempo_base_api_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {tempo_oauth_token}",
    }
    responses: List[httpx.Response] = []
    worklog_ids: List[int] = []
    async with httpx.AsyncClient() as client:
        async with anyio.create_task_group() as tg:
            for worklog in list_of_worklogs:
                tg.start_soon(
                    parse_and_create_worklog,
                    responses,
                    worklog_ids,
                    client,
                    worklog,
                    url,
                    headers,
                    author_account_id,
                )

    status_codes = [response.status_code for response in responses]

    results["status_codes"] = status_codes
    results["worklog_ids"] = worklog_ids
    return results


def make_async_create_worklog_requests(list_of_worklogs: List[WorklogModel]) -> None:
    """
    Run api post requests from list of WorklogsModels, run through anyio backend asyncio.

    :param value: validation string.
    :raises ValueError: when validator condition fails.
    :return: validation string.
    """
    return anyio.run(run_create_worklog_requests, list_of_worklogs, backend="asyncio")  # type: ignore
