from enum import Enum


class Providers(Enum):
    OPEN_METEO = "open_meteo"
    METEO_SOURCE = "meteo_source"


class SchemaMode(Enum):
    CURRENT = "current"
    HOURLY = "hourly"
