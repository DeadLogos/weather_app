import win32com.client
import requests
from typing import NamedTuple
from abc import ABC, abstractmethod
from execeptions import LocationAccessError, LocationProviderExistenceError
from enum import Enum
import dotenv
import os
import geopy
import sys
import re


dotenv.load_dotenv()


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


class Location(ABC):
    """
    Interface for any user location provider
    """
    @property
    @abstractmethod
    def coords(self) -> Coordinates:
        pass


class LocationIP(Location):
    """
    Provides user's coordinates by ip.
    Properties:
        coords: Coordinates
    """
    @staticmethod
    def _get_coordinates_by_ip() -> Coordinates:
        try:
            response = requests.get(os.getenv('LOCATION_SERVICE_PROVIDER_URL')).json()
            coords = response['loc'].split(',')
            return Coordinates(latitude=float(coords[0]), longitude=float(coords[1]))
        except (requests.exceptions.RequestException, TypeError, ValueError) as e:
            raise LocationAccessError(f'Failed to get location by IP: {e}')

    @property
    def coords(self) -> Coordinates:
        return self._get_coordinates_by_ip()


class LocationWindowsGPS(Location):
    """
    Provides user's coordinates by internal windows gps.
    Properties:
        coords: Coordinates
    """
    @staticmethod
    def _get_coordinates_by_windows_gps() -> Coordinates:
        try:
            gps = win32com.client.Dispatch('LocationDisp.DispLatLongReport')
            assert gps.Latitude != 0 and gps.Longitude != 0
            return Coordinates(latitude=gps.Latitude, longitude=gps.Longitude)
        except Exception as e:
            raise LocationAccessError(f'Failed to get location by Windows GPS: {e}')

    @property
    def coords(self) -> Coordinates:
        return self._get_coordinates_by_windows_gps()


class LocationGeopy(Location):
    """
    Provides user's coordinates by query(address).
    Properties:
        coords: Coordinates
    """
    def _get_coordinates_by_geopy(self) -> Coordinates:
        try:
            geolocator = geopy.Nominatim(user_agent='my-geolocator')
            query = self._get_geopy_query()
            location = geolocator.geocode(query)
            return Coordinates(latitude=location.latitude, longitude=location.longitude)
        except Exception as e:
            raise LocationAccessError(f'Failed to get location by geopy tools: {e}')

    @staticmethod
    def _get_geopy_query() -> str:
        if len(sys.argv) <= 2:
            return os.getenv('DEFAULT_GEOPY_QUERY')
        return ','.join(sys.argv[2:])

    @property
    def coords(self) -> Coordinates:
        return self._get_coordinates_by_geopy()


class LocationProviderMethod(Enum):
    IP = LocationIP
    GPS = LocationWindowsGPS
    QUERY = Q = LocationGeopy


def get_location() -> Coordinates:
    """
    Gets coordinates based on the chosen location provider method.
    Returns:
        Coordinates: latitude and longitude.
    """
    location_provider = _get_location_provider_method().value
    return location_provider().coords


def _get_location_provider_method() -> LocationProviderMethod:
    """
    Retrieves the location provider method from command-line arguments.
    If no arguments are passed, returns the default method (IP).
    Returns:
        LocationProviderMethod: Location provider method.
    """
    if len(sys.argv) == 1:
        return LocationProviderMethod.IP
    try:
        return LocationProviderMethod[_format_option(sys.argv[1])]
    except KeyError:
        raise LocationProviderExistenceError


def _format_option(arg: str) -> str:
    """
    Formats a command-line option by removing prefixed dashes and converting to uppercase.
    """
    return re.sub(r'^-{1,2}', '', arg).upper()


def main():
    pass


if __name__ == '__main__':
    main()
