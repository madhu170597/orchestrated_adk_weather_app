from google.adk.agents import Agent
from google.genai import types
from ...tools.constants import MODEL_NAME, TEMPERATURE

import requests

def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch complete weather data from Open-Meteo API for the given latitude and longitude.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        dict: Complete weather data for the location, including a generated summary.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current_weather=true"
        f"&hourly=temperature_2m,precipitation,wind_speed_10m"
        f"&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset"
        f"&timezone=auto"
    )
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        # Generate a detailed weather report
        current_weather = weather_data.get("current_weather", {})
        temperature = current_weather.get("temperature")
        wind_speed = current_weather.get("windspeed")
        wind_direction = current_weather.get("winddirection")
        weather_code = current_weather.get("weathercode")
        time = current_weather.get("time")

        # Map weather codes to descriptions (simplified example)
        weather_descriptions = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "foggy",
            48: "depositing rime fog",
            51: "light drizzle",
            61: "light rain",
            71: "light snow",
        }
        weather_description = weather_descriptions.get(weather_code, "unknown weather conditions")

        # Create a detailed report
        report = (
            f"The current temperature is {temperature}°C with {weather_description}. "
            f"The wind is blowing at a speed of {wind_speed} m/s from {wind_direction}°. "
            f"The weather data was last updated at {time}. "
            f"Stay prepared for the day ahead!"
        )

        # Add the report to the weather data
        weather_data["report"] = report
        print(type(weather_data))
        return weather_data
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code}, {response.text}")

get_act_weather_instruction = """
You are Weather Analyst. You will receive latitude and longitude for a city or place.
Your task:
    1. Use the latitude and longitude to get the current weather information for the city or place.
    2. Based on the latitude and longitude provided, call the weather tool `get_weather` to get the complete weather data.
        2.1 get_weather(latitude, longitude)
            it takes two arguments:
                latitude (float): Latitude of the location.
                longitude (float): Longitude of the location.
            returns: A dictionary containing complete weather data for the location, including a generated summary.
    3. Return the complete dictionary received from the `get_weather` tool back to the Orchestrator without modifying or filtering it.
    4. If you are not able to get the weather information, return "Weather information not found" back to the Orchestrator.
    5. Do not process, modify, or filter the data received from the `get_weather` tool. Simply return it as is.
    6. Do not include any explanations or additional information in the response. Only return the data received from the `get_weather` tool.
"""

weather_agent = Agent(
    name='weather_agent',
    model=MODEL_NAME,
    description=(
        "You are Weather Analyst. You will get the current weather information for a given city or place using `get_weather` tool and return it back to Orhcestrator."
    ),
    instruction=get_act_weather_instruction,
    tools=[get_weather],
    generate_content_config=types.GenerateContentConfig(
        temperature=TEMPERATURE,
    ),
)