from weather_service import WeatherInfo


def format_weather(data: WeatherInfo) -> str:
    """
    Formats weather data into a string for display.
    """
    input_info = (f'Location: {data.location.capitalize()}\n'
                  f'Temperature: {data.temperature}°C\n'
                  f'Weather condition: {data.description.name.lower()}\n'
                  f'Sunrise: {data.sunrise.strftime("%H:%M")}\n'
                  f'Sunset: {data.sunset.strftime("%H:%M")}')
    return input_info


def main():
    pass


if __name__ == '__main__':
    main()
