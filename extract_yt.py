import requests
from pprint import pprint
import json
from bs4 import BeautifulSoup as bs
from time import sleep


def main():
    """

    :return:
    """

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}

    requests.get("https://www.youtube.com", headers=header)
    scrape_url = "https://www.youtube.com"
    search_url = "/results?search_query="
    search_hardcode = "samsung+galaxy+s9"
    sb_url = scrape_url + search_url + search_hardcode

    sb_get = requests.get(sb_url, headers=header)
    soupeddata = bs(sb_get.content, "html.parser")
    yt_links = soupeddata.find_all("a", class_="yt-uix-tile-link")

    obj_href = []
    for i in yt_links:
        yt_title = i.get("title")
        yt_href = i.get("href")
        yt_final = scrape_url + yt_href
        obj_yt = {
            "title" : yt_title,
            "link" : yt_final
        }

        obj_href.append(obj_yt)

    pprint(obj_href)
    return obj_href

def executor(obj_href):
    """

    :return:
    """

    for row in obj_href:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
        r = requests.get(row["link"], headers=header)
        sleep(15)

        if r.status_code == 200:

            try:
                soupeddata = bs(r.content, "html.parser")
                views = soupeddata.find("span", attrs={'class': 'view-count'}).get_text()
                print(views)
                # likes_raw = soupeddata.select('.likes-count')[0].get_text().split()[0]

            except Exception:
                exit("Failed for scraping information")

        else:
            exit("Failed request to yt")



if __name__ == "__main__":
    obj_href = main()
    executor(obj_href)