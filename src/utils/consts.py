import pathlib

BASE_URL = "https://stormlightarchive.fandom.com"
WIKI_ALL_PAGES_URL = "https://stormlightarchive.fandom.com/wiki/Special:AllPages"
SRC_ROOT_PATH = pathlib.Path(__file__).parent.parent
PROJECT_ROOT = SRC_ROOT_PATH.parent
RAW_DATA_PATH = pathlib.Path(PROJECT_ROOT, "data/raw")
STOP_SCRAPING_URL = "https://stormlightarchive.fandom.com/wiki/Special:AllPages?from=Stargyle"
