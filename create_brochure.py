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


MODEL = 'gpt-4o-mini'
openai = OpenAI(api_key = api_key)

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# Create a class to represent a webpage
class Website:
    
    url: str
    title: str
    body: str
    links: List[str]
    text: str
    
    def __init__(self, url):
        self.url = url
        response = requests.get(url,headers = headers)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title Found"
        if soup.body:
            for irrelevant in soup.body("script","style","inputs","img"):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n",strip=True)
        else:
            self.text = ""
        links = [links.get('href') for links in soup.find_all('a')]
        self.links = [link for link in links if link]
    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"        

# Sytem Prompt contruction
link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"