from datetime import datetime

from pydantic import BaseModel, FilePath, field_validator


class WorklogModel(BaseModel):
    """Pydantic model for worklog entries."""

    issue: str
    time_spent: int
    start_date: str
    start_time: str

    @field_validator("time_spent", mode="before")
    def validate_time_spent(cls, value: str) -> int:  # noqa: N805, WPS111
        """
        Pydantic validation for issue field of time_spent.

        :param value: validation string.
        :raises ValueError: when validator condition fails.
        :return: validation string.
        """
        if not value.endswith("h") and not value.endswith("s"):
            raise ValueError('Time spent units must be in hours "h" or seconds "s"')
        try:
            time_unit_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
            float_from_string = float(value[:-1])
            time_unit = value[-1]
            time_spent_to_seconds = int(
                float_from_string * time_unit_dict[time_unit],
            )
        except ValueError:
            raise ValueError("Could not transform string to 24h hour string.")
        return time_spent_to_seconds

    @field_validator("start_date", mode="before")
    def validate_start_date(cls, value: str) -> str:  # noqa: N805, WPS111
        """
        Pydantic validation for issue field of start_date.

        :param value: validation string.
        :raises ValueError: when validator condition fails.
        :return: formatted date.
        """
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        return value

    @field_validator("start_time", mode="before")
    def validate_start_time(cls, value: str) -> str:  # noqa: N805, WPS111
        """
        Pydantic validation for issue field of start_time.

        :param value: validation string.
        :raises ValueError: when validator condition fails.
        :return: validation string.
        """
        try:
            datetime.strptime(value, "%H:%M:%S")
        except ValueError:
            raise ValueError("Incorrect time format, should be HH:MM:SS")
        return value


class CliArguments(BaseModel):
    """Pydantic model for cli args."""

    file_path: FilePath
