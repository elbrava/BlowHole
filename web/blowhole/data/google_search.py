import json
from time import sleep

list = ["symptoms", "prevention""treatment"]
from bs4 import BeautifulSoup
import requests
from googlesearch import search

dict_all = {}
with open("scrap.json", "r") as f:
    d = dict(json.load(f))
    for key in d.keys():
        query = key
        try:
            from googlesearch import search
            search("Google", num_results=100)

        except  Exception as e:
            print(str(e).split("url:")[1])
            r = requests.get(str(e).split("url:")[1])
            soup = BeautifulSoup(r.content, "lxml")
            print(soup.prettify())

        for title in (d[key]["mini_titles"]):
            print(title)
