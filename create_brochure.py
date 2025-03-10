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


openai = OpenAI(api_key = api_key)
ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

MODEL_OLLAMA = 'llama3.2'

MODEL = 'gpt-4o-mini'


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
        logger.info('get_contents called')
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"      

# Sytem Prompt contruction
link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""

# User Prompt
def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_links(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
      ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    logger.info('Get link function executed')
    return json.loads(result)


def get_all_details(url):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    logger.info("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result


# New system prompt

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."


def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt

# def create_brochure(company_name, url):
#     response = openai.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
#           ],
#     )
#     result = response.choices[0].message.content
#     logger.info('create_brochure executed')
#     display(Markdown(result))
    

def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
      ]
    stream = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


def stream_ollama(prompt):
    conversation = f"{system_prompt}\nUser: {prompt}\nAssistant:"
    stream = ollama.completions.create(
        model=MODEL_OLLAMA,
        prompt=conversation,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].text
        yield result

#create_brochure("HuggingFace", "https://huggingface.co")

