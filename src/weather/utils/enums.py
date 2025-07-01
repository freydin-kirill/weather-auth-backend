from enum import Enum


class SchemaMode(Enum):
    READ = "read"
    CURRENT = "current"
    HOURLY = "hourly"
