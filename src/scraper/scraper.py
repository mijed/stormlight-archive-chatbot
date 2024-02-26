from typing import Any

import requests
from bs4 import BeautifulSoup

from src.utils.consts import BASE_URL, WIKI_ALL_PAGES_URL


# TODO: Setup logger, writing text data to a file, data preprocessing


def extract_text_from_page(url: str) -> str:
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    main_text_div = soup.find("div", class_="mw-parser-output")
    paragraphs = main_text_div.find_all("p")

    text = "\n".join([p.get_text().strip() for p in paragraphs])

    return text


def get_all_hrefs(url: str) -> tuple[list, Any] | None:
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the <a> tags (links) on the webpage
        href_body = soup.find("div", class_="mw-allpages-body")
        links = href_body.find_all("a")

        # Extract href attributes from links
        hrefs = [link.get("href") for link in links]

        next_page_links = soup.find("div", class_="mw-allpages-nav").find_all("a")
        next_page_href = next_page_links[-1].get("href")

        return hrefs, next_page_href
    else:
        # If the request was not successful, print an error message
        print("Failed to retrieve data from the URL:", url)
        return None


next_page_url = WIKI_ALL_PAGES_URL
while next_page_url:
    hrefs, next_page_href = get_all_hrefs(next_page_url)
    print(f"Going to page: {next_page_href}")
    for link in hrefs[:3]:
        extracted_text = extract_text_from_page(BASE_URL + link)
        print(extracted_text)
        # Perform any other processing or saving of extracted_text here
    next_page_url = BASE_URL + next_page_href
