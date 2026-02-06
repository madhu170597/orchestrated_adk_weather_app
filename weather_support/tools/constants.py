from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME')
TEMPERATURE = 0.7