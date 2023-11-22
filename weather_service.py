import datetime
import requests
from abc import ABC, abstractmethod
from typing import Type
from enum import Enum
from dataclasses import dataclass, field
from geolocation import Coordinates
from execeptions import WeatherServiceAccessError
import dotenv
import os

dotenv.load_dotenv()


class WeatherDescription(Enum):
    """
    Weather's conditions
    """
    UNKNOWN = 'Нет данных'
    SNOW = 'Снег'
    RAIN = 'Дождь'
    CLEAR = 'Ясно'
    CLOUDS = 'Облачно'
    DRIZZLE = 'Изморозь'
    THUNDERSTORM = 'Гроза'
    MIST = FOG = 'Туман'
    HAZE = 'Легкий туман'
    DUST = ASH = SMOKE = SAND = 'Пыль'
    TORNADO = 'Торнадо'
    SQUALL = 'Шквал'

    @classmethod
    def get_descr(cls, name: str) -> 'WeatherDescription':
        try:
            return cls[name]
        except KeyError:
            return cls.UNKNOWN


Celsius = int
TownName = str


@dataclass(kw_only=True, frozen=True)
class WeatherInfo:
    """
    Weather data
    """
    temperature: Celsius
    location: TownName
    sunrise: datetime.datetime
    sunset: datetime.datetime
    description: WeatherDescription = field(default=WeatherDescription.UNKNOWN)


class WeatherAPI(ABC):
    """
    Interface for weather API with getting weather data by location
    """
    @abstractmethod
    def get_weather_data(self, coords: Coordinates) -> WeatherInfo:
        pass


class OpenWeatherAPI(WeatherAPI):
    def __init__(self):
        self._API_KEY = os.getenv('OPEN_WEATHER_API')
        self._url = os.getenv('OPEN_WEATHER_URL')

    def get_weather_data(self, coords: Coordinates) -> WeatherInfo:
        response = self._make_request_weather_service(coords)
        return self._parse_weather_service_response(response)

    def _make_request_weather_service(self, coords: Coordinates) -> requests.Response:
        parameters = {'lat': coords.latitude,
                      'lon': coords.longitude,
                      'appid': self._API_KEY,
                      'units': os.getenv('OPEN_WEATHER_UNITS'),
                      'lang': os.getenv('OPEN_WEATHER_LANGUAGE')
                      }
        try:
            return requests.get(url=self._url, params=parameters)
        except requests.exceptions.RequestException:
            raise WeatherServiceAccessError

    @staticmethod
    def _parse_weather_service_response(response: requests.Response) -> WeatherInfo:
        try:
            data = response.json()
            temp = round(data['main']['temp'])
            city = data['name']
            sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
            weather = WeatherDescription.get_descr(data['weather'][0]['main'].upper())
        except (requests.exceptions.RequestException, KeyError, TypeError, ValueError) as e:
            raise WeatherServiceAccessError
        return WeatherInfo(temperature=temp, location=city, sunrise=sunrise, sunset=sunset, description=weather)


def get_weather(coords: Coordinates, *, weather_service: Type[WeatherAPI] = OpenWeatherAPI) -> WeatherInfo:
    """
    Fetches weather data based on given coordinates using the specified weather service API.
    Args:
        coords (Coordinates): latitude and longitude.
        weather_service (Type[WeatherAPI]): API service providing weather data. Defaults to OpenWeatherAPI.
    Returns:
        WeatherInfo: Weather data including temperature, location, sunrise, sunset, and description.
    """
    return weather_service().get_weather_data(coords)


def main():
    pass


if __name__ == '__main__':
    main()
