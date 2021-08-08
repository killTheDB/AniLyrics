from urllib.parse import urlparse
import googlesearch
import requests
from bs4 import BeautifulSoup
import re

__BASE_URL__ = "www.animesonglyrics.com"


class NoLyricsFound(Exception):
    """Exception class to handle no lyrics found"""

    pass


class MissingTranslatedLyrics(Exception):
    """Exception class to handle lyrics with missing translated lyrics"""

    pass


class InvalidLanguage(ValueError):
    """Exception class to handle invalid language selection"""

    pass


def search_lyrics(query, lang="jp", show_title=False):
    url = get_lyrics_url(query)
    print(url)

    soup = get_lyrics_soup(url)
    # print(soup)

    if lang == "jp":
        lyrics_content = soup.find("div", attrs = {'id':'tab1'})
    elif lang == "en":
        lyrics_content = soup.find("div", attrs = {'id':'tab2'})
    else:
        raise InvalidLanguage("Unsupported language type")
    s=""
    for line in lyrics_content.get_text():
        s=s+line

    lyrics = re.sub(' +', ' ', s)
    # print(lyrics)

    song_title = get_song_info(soup)

    return lyrics,song_title


def get_song_info(soup):
    title = soup.find("a", {"class": "SngLnk2"})
    return title.get_text()


def get_lyrics_soup(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")

    # convert all br into newlines
    for line_break in soup.find_all("br"):
        line_break.replace_with("\n")

    # # remove all unwanted tags in the page
    for div in soup.find_all("div", {'class':'correct'}): 
        div.decompose()

    tags_to_remove = ["dt", "sup","style","script","input","form","button","label","span"]

    for tag_name in tags_to_remove:
        for tag in soup.find_all(tag_name):
            tag.decompose()
    return soup


def get_lyrics_url(query):
    for url in googlesearch.search("site:{} {}".format(__BASE_URL__, query), stop=10):
        # return the first page with .htm in the url as it contains lyrics
        # if str(url).endswith(".htm"):
        #     return url
        return url

    # return none if query cannot find any pages
    raise NoLyricsFound
