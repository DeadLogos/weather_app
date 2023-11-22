import json
import pathlib
from typing import TypedDict, Type
from weather_service import WeatherInfo, Celsius, TownName
from abc import ABC, abstractmethod
import datetime
import dotenv
import os

dotenv.load_dotenv()


class WeatherLogger(ABC):
    """
    Interface for logging results of application work
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def make_log(self, weather: WeatherInfo) -> None:
        pass


TimeFormat = str  # HH:MM


class JSONWeatherFormat(TypedDict):
    location: TownName
    temperature: Celsius
    description: str
    sunrise: TimeFormat
    sunset: TimeFormat


IsoFormatStr = str  # YYYY-MM-DD HH:MM:SS


class JSONRecordFormat(TypedDict):
    date: IsoFormatStr
    weather: JSONWeatherFormat


class JSONWeatherLogger(WeatherLogger):
    """
    Logging weather in a json file
    """
    def __init__(self):
        self._file = pathlib.Path(pathlib.Path.cwd(), os.getenv('JSON_LOG_FILE'))
        if not self._file.exists():
            with open(self._file, 'w', encoding='utf-8') as file:
                json.dump([], file)

    def make_log(self, weather: WeatherInfo) -> None:
        data = self._make_json_format_data(weather)
        self._write_json(data)

    @staticmethod
    def _make_json_format_data(weather: WeatherInfo) -> JSONRecordFormat:
        date = datetime.datetime.now().isoformat(sep=' ').split('.')[0]
        weather_info = JSONWeatherFormat(
            location=weather.location,
            temperature=weather.temperature,
            description=weather.description.name,
            sunrise=weather.sunrise.strftime('%H:%M'),
            sunset=weather.sunset.strftime('%H:%M')
        )
        return JSONRecordFormat(date=date, weather=weather_info)

    def _read_json(self) -> list[JSONRecordFormat]:
        with open(self._file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _write_json(self, date: JSONRecordFormat) -> None:
        storage = self._read_json()
        storage.append(date)
        with open(self._file, 'w', encoding='utf-8') as file:
            json.dump(storage, file, ensure_ascii=False, indent=4)


def log(weather: WeatherInfo, *, logger: Type[WeatherLogger] = JSONWeatherLogger) -> None:
    """
    Logs weather information using the specified logger.
    Args:
        weather (WeatherInfo): Weather information to be logged.
        logger (Type[WeatherLogger]: Logger to be used for logging. Defaults to JSONWeatherLogger.
    """
    logger().make_log(weather)


def main():
    pass


if __name__ == '__main__':
    main()
