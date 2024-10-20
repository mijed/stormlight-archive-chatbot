from typing import Any

import requests
from bs4 import BeautifulSoup
from src.utils.consts import BASE_URL, WIKI_ALL_PAGES_URL, RAW_DATA_PATH, STOP_SCRAPING_URL
from src.logging.logger import logger
import polars as pl
import os


def extract_text_from_page(url: str) -> str:
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    main_text_div = soup.find("div", class_="mw-parser-output")
    paragraphs = main_text_div.find_all("p")

    text = "\n".join([p.get_text().strip() for p in paragraphs])

    return text


def get_all_hrefs(url: str) -> tuple[list, Any] | None:
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        href_body = soup.find("div", class_="mw-allpages-body")
        links = href_body.find_all("a")

        hrefs = [link.get("href") for link in links]

        next_page_links = soup.find("div", class_="mw-allpages-nav").find_all("a")
        next_page_href = next_page_links[-1].get("href")

        return hrefs, next_page_href
    else:
        logger.error("Failed to retrieve data from the URL:", url)
        raise


output_file = RAW_DATA_PATH / "stormlight_wiki_raw_text_data.csv"
if not os.path.isfile(output_file):
    pl.DataFrame({"url": [], "text": []}).write_csv(output_file, separator=";")


data_df = pl.DataFrame({"url": [], "text": []})
next_page_url = WIKI_ALL_PAGES_URL
while next_page_url != STOP_SCRAPING_URL:
    hrefs, next_page_href = get_all_hrefs(next_page_url)
    logger.info(f"Going to page: {next_page_href}")
    for link in hrefs:
        full_link = BASE_URL + link
        extracted_text = extract_text_from_page(full_link)
        logger.info(f"Extracted text from page: {full_link}")
        data_df = pl.concat(
            [data_df, pl.DataFrame({"url": [full_link], "text": [extracted_text]})],
            how="diagonal_relaxed",
        )

    with open(output_file, mode="ab") as f:
        data_df.write_csv(f, separator=";")
    logger.info(f"Saved raw data from {len(hrefs)} pages to {output_file}.")
    next_page_url = BASE_URL + next_page_href
