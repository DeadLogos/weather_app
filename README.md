# Weather Forecast App

This Python application provides weather information based on user coordinates obtained from various sources such as IP, GPS, or location queries.

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/DeadLogos/weather_app.git
    ```

2. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up environment variables:
   
   - Create a `.env` file in the project directory.
   - Add the necessary environment variables:

    ```
    OPEN_WEATHER_API=your_open_weather_api_key
    JSON_LOG_FILE=weather_logs.json
    DEFAULT_GEOPY_QUERY=your_default_location
    OPEN_WEATHER_URL='https://api.openweathermap.org/data/2.5/weather'
    OPEN_WEATHER_LANGUAGE='en'
    OPEN_WEATHER_UNITS='metric'
    LOCATION_SERVICE_PROVIDER_URL='https://ipinfo.io'
    ```

## Usage

Run the application using the following command:

```
python main.py
This will prompt you to specify a method for obtaining location information. Use the following flags:

--ip for IP-based location retrieval.
--gps for GPS-based location retrieval.
--query (--q) "Your location" for querying a specific location.
```

## Structure

### The application structure is as follows:

 - main.py: Entry point of the application.
 - geolocation.py: Module for obtaining user location.
 - weather_service.py: Module for fetching weather information.
 - weather_output_handler.py: Module for formatting weather output.
 - logger.py: Module for logging weather information.