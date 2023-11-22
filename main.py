from geolocation import get_location
from weather_service import get_weather
from weather_output_handler import format_weather
from logger import log
from execeptions import *


def main():
    """
    Main function of the application.
    Retrieves user's location and fetches weather information based on the location.
    Prints formatted weather data.
    """
    try:
        coords = get_location()
    except (LocationAccessError, LocationProviderExistenceError):
        print('Failed to get gps coordinates')
        exit(1)
    try:
        data = get_weather(coords)
    except WeatherServiceAccessError:
        print(f'Failed to get weather data by {coords}')
        exit(1)
    formatted_data = format_weather(data)
    print(formatted_data)
    log(data)


if __name__ == '__main__':
    main()
