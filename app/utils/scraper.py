import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def send_requests(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    return soup


