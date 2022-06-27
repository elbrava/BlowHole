import json

import requests

med = ["symptoms", "prevention","treatment"]
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch

que = 'NoCopyrightSounds'

link_dict = {}


def main():
    with open("scrap.json", "r") as f:
        d = dict(json.load(f))
        for key in d.keys():
            que = key
            link_dict[que] = {}

            link_dict[que]["intro"] = get_url(que)
            link_dict[que]["categories"] = {}
            for title in (d[key]["mini_titles"]):
                link_dict[que]["categories"][title] = {}
                for m in med:
                    link_dict[que]["categories"][title][m] = get_url(title + f" {m}")
    with open("video.json", "w") as f:
        json.dump(link_dict, f)

    print(link_dict)


def get_url(query):
    videosSearch = VideosSearch(query, limit=4)
    links = []
    d = videosSearch.result()["result"]
    for i in d:
        print(i["link"])
        links.append(i["link"])

    return links


# with open("gg.json", "w") as f:

if __name__ == '__main__':
    main()
