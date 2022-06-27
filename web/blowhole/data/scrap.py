from bs4 import BeautifulSoup
import requests
import json

URL = "https://www.verywellmind.com/a-list-of-psychological-disorders-2794776"
r = requests.get(URL)
soup = BeautifulSoup(r.content, "lxml")
s = soup.find_all("div", class_=r"comp content-list-sc mntl-sc-list-item mntl-sc-page mntl-block")
dict_all = {}
with open("scrap.json", 'w') as f:
    content_paragraphs = []
    for d in s:

        content_paragraphs = []
        main_title = d.h2.span.text
        dict_all[main_title] = {}
        dict_all[main_title]["mini_titles"] = []
        mini_titles = d.find_all("h3")
        pps = d.find_all("p")

        print(" ")
        print(main_title)
        print("")
        try:
            for h in mini_titles:
                dict_all[main_title]["mini_titles"].append(h.span.text.strip())
                print(h.span.text)
        except AttributeError:
            mini_titles = d.find("ul")
            mini_titles = mini_titles.find_all("li")
            for h in mini_titles:
                print(h.strong.text)
                dict_all[main_title]["mini_titles"].append(h.strong.text)

                # print(h.a.strong.text)
        for p in pps:
            print(p.text)
            content_paragraphs.append(str(p))

        dict_all[main_title]["content"] = content_paragraphs

        # sub_titles_dict={
        # }

        # print(title)
        # introduction=
    print(dict_all)
    json.dump(dict_all,f)
"""
    print(s.prettify())
    print()
    print(d.prettify())
    print(" ")
"""
