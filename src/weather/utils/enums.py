from enum import Enum


class SchemaMode(Enum):
    """Modes for representing weather data."""

    READ = "read"
    CURRENT = "current"
    HOURLY = "hourly"
