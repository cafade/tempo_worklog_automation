import pytest

from tempo_worklog_automation.src.math import my_sum


@pytest.mark.anyio
async def test_my_sum() -> None:
    """
    Test my_sum function.

    GIVEN two integers
    WHEN my_sum is called
    THEN the sum of the two must be returned
    """
    assert my_sum(4, 1) == 5
