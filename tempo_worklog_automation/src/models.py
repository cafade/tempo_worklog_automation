from datetime import datetime

from pydantic import BaseModel, validator


class IssueModel(BaseModel):
    """Pydantic model for worklog issues."""

    issue: str
    time_spent: int
    start_date: str
    start_time: str

    @validator("time_spent", pre=True)
    def validate_time_spent(cls, v: str) -> int:  # noqa: N805, WPS111
        """
        Pydantic validation for issue field of time_spent.

        :param v: validation string.
        :raises ValueError: when validator condition fails.
        :return: validation string.
        """
        if not v.endswith("h") and not v.endswith("s"):
            raise ValueError('Time spent units must be in hours "h" or seconds "s"')
        try:
            time_unit_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
            float_from_string = float(v[:-1])
            time_unit = v[-1]
            time_spent_to_seconds = int(
                float_from_string * time_unit_dict[time_unit],
            )
        except ValueError:
            raise ValueError("Could not transform string to 24h hour string.")
        return time_spent_to_seconds

    @validator("start_date", pre=True)
    def validate_start_date(cls, v: str) -> str:  # noqa: N805, WPS111
        """
        Pydantic validation for issue field of start_date.

        :param v: validation string.
        :raises ValueError: when validator condition fails.
        :return: formatted date.
        """
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        return v

    @validator("start_time", pre=True)
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
