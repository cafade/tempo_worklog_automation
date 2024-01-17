from datetime import datetime

from pydantic import BaseModel, Field, validator


class IssueModel(BaseModel):
    """Pydantic model for worklog issues."""

    issue: str
    time_spent: str = Field(...)
    start_date: str
    start_time: str

    @validator("time_spent")
    def validate_time_spent(cls, v: str) -> str:  # noqa: N805, WPS111
        """
        Pydantic validation for issue field of time_spent.

        :param v: validation string.
        :raises ValueError: when validator condition fails.
        :return: validation string.
        """
        if not v.endswith("h") and not v.endswith("s"):
            raise ValueError('Time spent units must be in hours "h" or seconds "s"')
        return v

    @validator("start_date")
    def validate_start_date(cls, v: str) -> str:  # noqa: N805, WPS111
        """
        Pydantic validation for issue field of start_date.

        :param v: validation string.
        :raises ValueError: when validator condition fails.
        :return: validation string.
        """
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        return v

    @validator("start_time")
    def validate_start_time(cls, v: str) -> str:  # noqa: N805, WPS111
        """
        Pydantic validation for issue field of start_time.

        :param v: validation string.
        :raises ValueError: when validator condition fails.
        :return: validation string.
        """
        try:
            datetime.strptime(v, "%H:%M:%S")
        except ValueError:
            raise ValueError("Incorrect time format, should be HH:MM:SS")
        return v
