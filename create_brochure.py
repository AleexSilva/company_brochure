import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI
from logger import logger

# Initialize and constants

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

# check the API key
if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    logger.info("API key looks good so far")
else:
    logger.error("There might be a problem with your API key? Please visit the troubleshooting notebook!")


