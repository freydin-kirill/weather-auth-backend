from src.weather.adapters.base import BaseWeatherAdapter
from src.weather.adapters.meteo_source import MeteoSourceAdapter
from src.weather.adapters.open_meteo import OpenMeteoAdapter
from src.weather.schemas.base import BaseWeatherSchema, BaseWriteWeatherSchema
from src.weather.schemas.meteo_source import (
    SCurrentMeteoSourceData,
    SHourlyMeteoSourceData,
    SWriteMeteoSourceData,
)
from src.weather.schemas.open_meteo import SCurrentOpenMeteoData, SHourlyOpenMeteoData, SWriteOpenMeteoData
from src.weather.utils import ProviderEnum, SchemaModeEnum


def get_provider(name: ProviderEnum) -> type[BaseWeatherAdapter]:
    providers: dict[str, type[BaseWeatherAdapter]] = {
        ProviderEnum.OPEN_METEO.value: OpenMeteoAdapter,
        ProviderEnum.METEO_SOURCE.value: MeteoSourceAdapter,
    }
    try:
        return providers[name.value]
    except KeyError:
        raise ValueError(
            f"Provider '{name.value}' not found. Available providers: {', '.join(providers.keys())}"
        )


def get_schema_by_provider(
    name: ProviderEnum, mode: SchemaModeEnum = SchemaModeEnum.CURRENT
) -> type[BaseWeatherSchema]:
    schemas: dict[str, dict[str, type[BaseWeatherSchema]]] = {
        ProviderEnum.OPEN_METEO.value: {
            SchemaModeEnum.CURRENT.value: SCurrentOpenMeteoData,
            SchemaModeEnum.HOURLY.value: SHourlyOpenMeteoData,
        },
        ProviderEnum.METEO_SOURCE.value: {
            SchemaModeEnum.CURRENT.value: SCurrentMeteoSourceData,
            SchemaModeEnum.HOURLY.value: SHourlyMeteoSourceData,
        },
    }
    try:
        return schemas[name.value][mode.value]
    except KeyError:
        raise ValueError(
            f"Schema for provider '{name}' not found. Available schemas: {', '.join(schemas.keys())}"
        )


def get_write_schema_by_provider(name: ProviderEnum) -> type[BaseWriteWeatherSchema]:
    schemas: dict[str, type[BaseWriteWeatherSchema]] = {
        ProviderEnum.OPEN_METEO.value: SWriteOpenMeteoData,
        ProviderEnum.METEO_SOURCE.value: SWriteMeteoSourceData,
    }
    try:
        return schemas[name.value]
    except KeyError:
        raise ValueError(
            f"Write schema for provider '{name}' not found. Available schemas: {', '.join(schemas.keys())}"
        )
