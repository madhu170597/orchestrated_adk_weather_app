from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types
from ...tools.constants import MODEL_NAME, TEMPERATURE

weather_query_rewriter_instruction = """You are Weather Analyst. You will receive an user query requesting some assitance with respect to a city or a place he is interested.
Your task:
    1. Understand the user query and extract the city or place name from it.
    2. Use the google search tool to find the latitude and longitude of the city or place.
    3. Once you have the lattitude and longitude, rewrite all the information that user has asked about the city or place in a machine readable format without any ambiguity and return the response back to Orhcestrator.
    4. If you are not able to find the city or place name, return "City or place name not found" back to Orchestrator.
    5. If you are not able to find the latitude and longitude, return "Latitude and Longitude not found" back to Orchestrator.
        In both 4 and 5, also include the city or place name if you have found it.
        {
            "city_or_place_name": "name of the city or place if you have found it, else return null",
            "error_message": "City or place name not found" OR "Latitude and Longitude not found"        
        }
    6. If you find the city or place name and its latitude and longitude, return the response in the following format:
    {
        "city_or_place_name": "name of the city or place",
        "latitude": "latitude value",
        "longitude": "longitude value",
        "other_information": "any other information that user has asked about the city or place"
    }
    7. Make sure the response is in the above format and is machine readable without any ambiguity.
    8. Do not include any explanations or additional information in the response, only return the information in the above format.
    9. Do not assume anything that is not explicitly mentioned in the user query, only extract and return the information that is asked by the user.
"""

weather_query_rewriter = LlmAgent(
    model=MODEL_NAME,
    name='weather_query_rewriter',
    description="""You are Weather Analyst. You will simplyfy the user query and understand what is needed and return the response back to Orhcestrator.""",
    instruction=weather_query_rewriter_instruction,
    generate_content_config=types.GenerateContentConfig(
        temperature=TEMPERATURE,
    ),
    tools =[google_search]
)