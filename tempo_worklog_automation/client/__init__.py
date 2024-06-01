"""Tempo worklog api client."""
import logging
from typing import Any, Dict, List, Optional

import anyio
import httpx

from tempo_worklog_automation.client.models import WorklogModel
from tempo_worklog_automation.settings import settings

logger = logging.getLogger(settings.logger_name)


async def delete_worklog(  # noqa: WPS211, WPS231
    responses: List[httpx.Response],
    worklog_id: int,
    client: httpx.AsyncClient,
    url: str,
    headers: Dict[str, str],
    max_retries: int = 5,
    backoff_factor: float = 0.5,
) -> Optional[httpx.Response]:
    """
    Perform api call to delete worklog by id. Retries n times when being throttled.

    :param responses: empty list of httpx.Response to store them.
    :param worklog_id: specific worklog id to be deleted.
    :param client: instance of httpx.AsyncClient.
    :param url: url for Tempo api endpoint.
    :param headers: dictionary with key value pairs for each header in request.
    :param max_retries: int for the number of retries for the request.
    :param backoff_factor: float for the exponential wait period.
    :raises httpx.HTTPStatusError: when request returns an http error code.
    :raises httpx.RequestError: when request fails.
    :return: httpx.Response or None.
    """
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
            if exc.response.status_code == 429:  # noqa: WPS432
                wait_time = backoff_factor * (2**attempt)
                logger.debug(
                    f"Received HTTP  429 - Too Many Requests. Retrying in {wait_time} seconds...",  # noqa: E501
                )
                await anyio.sleep(wait_time)
            else:
                decoded_content = exc.response.content.decode("utf-8")
                logger.debug(
                    f"Error response {exc.response.status_code!r} while requesting {exc.request.url!r}.\n\t{decoded_content}",  # noqa: E501, WPS237
                )
                raise
        except httpx.RequestError as exc:
            logger.debug(
                f"An error occurred while requesting {exc.request.url!r}.",  # noqa: E501, WPS237
            )
            raise

    logger.debug(f"All retries failed for {worklog_id}.")
    return None


async def run_delete_worklog_requests(
    worklog_ids: List[int],
) -> List[int]:
    """
    Run api delete requests from list of worklog ids, run through anyio backend asyncio.

    :param worklog_ids: ints list of worklog ids to delete.
    :return: list of http response codes.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.tempo_oauth_token}",
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
                    settings.tempo_base_api_url,
                    headers,
                )

    return [response.status_code for response in responses]


def make_async_delete_worklog_requests(worklog_ids: List[int]) -> None:
    """
    Run api delete requests from list of worklog ids, run through anyio backend asyncio.

    :param worklog_ids: ints list of worklog ids to delete.
    :return: None.
    """
    logger.info("running make_async_delete_worklog_requests")

    return anyio.run(run_delete_worklog_requests, worklog_ids, backend="asyncio")  # type: ignore # noqa: E501


async def get_issue_id(issue_name: str) -> int:
    """
    Run Jira api request request to get the issue / worklog internal id from the issue_name, run through anyio backend asyncio.

    :param issue_name: string for the issue / worklog name.
    :return: Int with the issue / worklog internal id..
    """  # noqa: E501
    url = f"{settings.jira_base_api_url}/{issue_name}"
    auth = (settings.jira_account_email, settings.jira_token)
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=headers, auth=auth)

    return response.json()["id"]


async def parse_worklog(
    worklog: WorklogModel,
    author_account_id: str,
) -> Dict[str, Any]:
    """
    Parse an worklog name string, get the corresponding issue / worklog internal id int.

    :param worklog: worklog model to parse for internal id.
    :param author_account_id: author account id to use when creating the worklog.
    :return: parsed_worklog: new object that contains int of internal issue id.
    """
    issue_id = await get_issue_id(worklog.issue)
    return {
        "authorAccountId": author_account_id,
        "description": worklog.issue,
        "issueId": issue_id,
        "startDate": worklog.start_date,
        "startTime": worklog.start_time,
        "timeSpentSeconds": worklog.time_spent,
    }


async def parse_and_create_worklog(  # noqa: WPS211, WPS231
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
    """
    Parse and create worklog.

    Call parse_worklog() for the new worklog object to be created and perform a post
    request to tempo API endpoint with the object and authentication headers.

    :param responses: empty list of httpx.Response to store them.
    :param worklog_ids: empty list of ints to store the corresponding internal id.
    :param client: instance of httpx.AsyncClient.
    :param worklog: instance worklog model inside list_of_worklogs.
    :param url: url for Tempo api endpoint.
    :param headers: dictionary with key value pairs for each header in request.
    :param author_account_id: author account id to use when creating the worklog.
    :param max_retries: int for the number of retries for the request.
    :param backoff_factor: float for the exponential wait period.
    :raises httpx.HTTPStatusError: when request returns an http error code.
    :raises httpx.RequestError: when request fails.
    :return: httpx.Response: response code from post request for issue creation or None.
    """
    parsed_worklog = await parse_worklog(worklog, author_account_id)

    for attempt in range(max_retries):
        try:
            response = await client.post(
                url=url,
                headers=headers,
                json=parsed_worklog,
            )
            responses.append(response)
            response.raise_for_status()
            worklog_ids.append(response.json()["tempoWorklogId"])
            return response

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:  # noqa: WPS432
                wait_time = backoff_factor * (2**attempt)
                logger.debug(
                    f"Received HTTP  429 - Too Many Requests. Retrying in {wait_time} seconds...",  # noqa: E501
                )
                await anyio.sleep(wait_time)
            else:
                decoded_content = exc.response.content.decode("utf-8")
                logger.debug(
                    f"Error response {exc.response.status_code!r} while requesting {exc.request.url!r}.\n\t{decoded_content}",  # noqa: WPS237, E501
                )
                raise
        except httpx.RequestError as exc:
            logger.debug(f"An error occurred while requesting {exc.request.url!r}.")
            raise

    logger.debug(f"All retries failed for {parsed_worklog}.")
    return None


async def run_create_worklog_requests(
    list_of_worklogs: List[WorklogModel],
) -> Dict[str, Any]:
    """
    Run api post requests from list of WorklogsModels. Call anyio.create_task_group().

    :param list_of_worklogs: list of WorklogModel objects.
    :return: list of http response codes.
    """
    results: Dict[str, Any] = {"status_codes": [], "worklog_ids": []}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.tempo_oauth_token}",
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
                    settings.tempo_base_api_url,
                    headers,
                    settings.author_account_id,
                )

    status_codes = [response.status_code for response in responses]

    results["status_codes"] = status_codes
    results["worklog_ids"] = worklog_ids
    return results


def make_async_create_worklog_requests(list_of_worklogs: List[WorklogModel]) -> None:
    """
    Run api post requests from list of WorklogsModels through anyio backend asyncio.

    :param list_of_worklogs: list of WorklogsModels to use in requests.
    :return: None.
    """
    logger.info("running make_async_create_worklog_requests")

    return anyio.run(  # type: ignore
        run_create_worklog_requests,  # type: ignore
        list_of_worklogs,
        backend="asyncio",
    )
