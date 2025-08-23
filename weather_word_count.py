import os
import logging

from boto3 import session
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import http_request

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv("config_files/.env")

WEATHER_SYSTEM_PROMPT = """You are a weather assistant with HTTP capabilities. You can:

1. Make HTTP requests to the National Weather Service API
2. Process and display weather forecast data
3. Provide weather information for locations in the United States

When retrieving weather information:
1. First get the coordinates or grid information using [https://api.weather.gov/points/{latitude},{longitude}](https://api.weather.gov/points/%7Blatitude%7D,%7Blongitude%7D) or [https://api.weather.gov/points/{zipcode}](https://api.weather.gov/points/%7Bzipcode%7D)
2. Then use the returned forecast URL to get the actual forecast

When displaying responses:
- Format weather data in a human-readable way
- Highlight important information like temperature, precipitation, and alerts
- Handle errors appropriately
- Convert technical terms to user-friendly language

Always explain the weather conditions clearly and provide context for the forecast.

IMPORTANT: When asked to count words, you MUST use the word_count tool on the FINAL weather response text.
"""


@tool
def word_count(text: str) -> int:
    """Count words in text."""
    logging.info(f"🔧 WORD_COUNT TOOL CALLED")
    logging.info(f"📝 Input text length: {len(text)} characters")
    logging.info(f"📝 Input text preview: {text[:100]}...")
    
    word_count_result = len(text.split())
    logging.info(f"📊 Word count result: {word_count_result}")
    
    return word_count_result


bedrock_model = BedrockModel(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    boto_session=session.Session(
        aws_access_key_id=os.getenv("aws_access_key_id", ""),
        aws_secret_access_key=os.getenv("aws_secret_access_key", ""),
        region_name=os.getenv("aws_region", ""),
    ),
    # streaming=False, #uncomment to see new error
)

agent = Agent(
    system_prompt=WEATHER_SYSTEM_PROMPT,
    tools=[word_count, http_request],
    model=bedrock_model,
    name="weather_word_count_agent",
)

logging.info("🚀 Starting weather agent...")

response = agent(
    "What's the weather like in Washington D.C? Also how many words are in the response?"
)

logging.info("✅ Agent execution completed!")
print(response)
