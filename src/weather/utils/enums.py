from enum import Enum


class Providers(Enum):
    OPEN_METEO = "open_meteo"
    METEO_SOURCE = "meteo_source"
    TOMORROW_IO = "tomorrow_io"


class ProvidersMode(Enum):
    READ = "read"
    CURRENT = "current"
    HOURLY = "hourly"
