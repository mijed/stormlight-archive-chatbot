from bs4 import BeautifulSoup
import requests

url = "https://stormlightarchive.fandom.com/wiki/Dalinar_Kholin"


def extract_text_from_page(url: str) -> str:
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    main_text_div = soup.find('div', class_='mw-parser-output')
    paragraphs = main_text_div.find_all('p')

    text = '\n'.join([p.get_text().strip() for p in paragraphs[1:-1]])

    return text


def get_all_hrefs(url: str) -> list[str] | None:
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the <a> tags (links) on the webpage
        href_body = soup.find('div', class_='mw-allpages-body')
        links = href_body.find_all('a')

        # Extract href attributes from links
        hrefs = [link.get('href') for link in links]

        return hrefs
    else:
        # If the request was not successful, print an error message
        print("Failed to retrieve data from the URL:", url)
        return None

print(get_all_hrefs("https://stormlightarchive.fandom.com/wiki/Special:AllPages"))