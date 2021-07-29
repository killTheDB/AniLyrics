# coding: utf-8
from urllib.parse import urlparse
from scrapingbee import ScrapingBeeClient
import googlesearch
import requests
from bs4 import BeautifulSoup

__BASE_URL__ = "www.animelyrics.com"


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
    """
    Search the given query string inside AnimeLyrics.

    :param str query: Query string. 
    :param str lang: Language to search in (jp, en)
    :param bool show_title: Show title at the top of the string

    :rtype: str
    :return: String of lyrics in given language
    """
    if lang != "en" and lang != "jp":
        raise InvalidLanguage("Unsupported language type")

    if lang == "jp":
        class_name = "romaji"
        song_idx = 0
    elif lang == "en":
        class_name = "translation"
        song_idx = 1

    url = get_lyrics_url(query)
    print(url)
    soup = get_lyrics_soup(url)

    center_box = soup.find("div", {"class": "centerbox"})

    lyrics_table = center_box.find("table")
    print(lyrics_table)
    lyrics = ""

    if lyrics_table is None:
        if lang == "en":
            raise MissingTranslatedLyrics("No translated lyrics found")

        lyrics = center_box.find("span", {"class": "lyrics"}).get_text()
    else:
        lyrics_divs = lyrics_table.find_all("td", {"class": class_name})
        print(lyrics_divs)
        for div in lyrics_divs:
            lyrics += div.get_text()

    # remove trailing spaces and weird space
    # lyrics = lyrics.replace("\xa0", " ").strip()

    # remove whitespaces from each line
    print(lyrics)
    # stripped_lines = [line.strip() for line in lyrics.splitlines()]
    # lyrics = "\n".join(stripped_lines)

    if show_title:
        song_name, anime_name = get_song_info(soup)

        # song name might be english
        # set index to japanese name if english name not found
        if lang == "en" and len(song_name) == 1:
            song_idx = 0

        return "{} - {}\n\n{}".format(song_name[song_idx], anime_name, lyrics)
    else:
        return lyrics


def get_song_info(soup):
    """
    Retrieve the song name (english / japanese) and anime name

    :param BeautifulSoup soup: BeautifulSoup4 object of lyrics url

    :rtype [str, str]
    :return Tuple of song and anime name
    """
    crumbs = soup.find("ul", {"id": "crumbs"})
    crumbs_list = crumbs.find_all("li")
    song_name = [name.strip() for name in crumbs_list[-1].get_text().split("-")]
    anime_name = crumbs_list[-2].get_text()

    return (song_name, anime_name)


def get_lyrics_soup(url):
    """
    Get a BeautifulSoup4 representation of a url

    :param str url: URL to read

    :rtype: BeautifulSoup
    :return: BeautifulSoup4 object of the loaded url
    """
    client = ScrapingBeeClient(api_key='40VNWM7NYZH6HVMAJW43OXXW92FK5I80Q4QJXBHWG6832SJT0ZV3BH60L246FKPGXFGNXYCL75PUQYWA')
    response = client.get(
        url,
        params={ 
            'render_js': 'false',  
        },         
    )
    # html_text = requests.get(url).text
    html_text = response.content
    soup = BeautifulSoup(html_text, "lxml")

    # convert all br into newlines
    # for line_break in soup.find_all("br"):
    #     line_break.replace_with("\n")


    # remove all unwanted tags in the page
    tags_to_remove = ["dt", "sup"]

    for tag_name in tags_to_remove:
        for tag in soup.find_all(tag_name):
            tag.decompose()
    
    # print(soup)
    return soup


def get_lyrics_url(query):
    """
    Finds a url in AnimeLyrics website for a lyric

    :param str query: Query string.

    :rtype: str
    :return: String of the url page for the given query
    """
    for url in googlesearch.search("site:{} {}".format(__BASE_URL__, query), stop=10):
        # return the first page with .htm in the url as it contains lyrics
        if str(url).endswith(".htm"):
            print(url)
            return url

    # return none if query cannot find any pages
    raise NoLyricsFound("Lyrics not found")
