from enum import Enum


class Providers(Enum):
    OPEN_METEO = "open_meteo"
    METEO_SOURCE = "meteo_source"


class SchemaMode(Enum):
    READ = "read"
    CURRENT = "current"
    HOURLY = "hourly"
