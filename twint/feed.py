from bs4 import BeautifulSoup
from re import findall
from json import loads

import logging as logme
import lxml

def Follow(response):
    logme.debug(__name__+':Follow')
    soup = BeautifulSoup(response, "html.parser")
    follow = soup.find_all("td", "info fifty screenname")
    cursor = soup.find_all("div", "w-button-more")
    try:
        cursor = findall(r'cursor=(.*?)">', str(cursor))[0]
    except IndexError:
        logme.critical(__name__+':Follow:IndexError')

    return follow, cursor

def Mobile(response):
    logme.debug(__name__+':Mobile')
    soup = BeautifulSoup(response, "lxml")
    tweets = soup.find_all("span", "metadata")
    max_id = soup.find_all("div", "w-button-more")
    try:
        max_id = findall(r'max_id=(.*?)">', str(max_id))[0]
    except Exception as e:
        #print(__file__,':Mobile:' + str(e), str(max_id))
        ...

    return tweets, max_id

def profile(response):
    logme.debug(__name__+':profile')
    json_response = loads(response)
    html = json_response["items_html"]
    soup = BeautifulSoup(html, "lxml")
    feed = soup.find_all("div", "tweet")

    return feed, feed[-1]["data-item-id"]

def Json(response):
    logme.debug(__name__+':Json')
    json_response = loads(response)
    html = json_response["items_html"]
    soup = BeautifulSoup(html, "html.parser")
    feed = soup.find_all("div", "tweet")
    return feed, json_response["min_position"]
