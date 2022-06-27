import json
import os

import youtube_dl
from pafy import pafy

base_dir = os.getcwd()


def main():
    dict_all = {}
    with open("video.json", "r") as f:
        d = dict(json.load(f))
        for key in d.keys():
            query = key
            print(key)
            # intro
            intro_list = d[key]["intro"]
            for intro in intro_list:
                directory = base_dir + r"\vid" + f"\{key[1:-2]}" + "\intro"
                print(directory)
                try:
                    os.chdir(directory)
                except:
                    os.makedirs(directory)
                    os.chdir(directory)

                down(intro)
            print(d[key]["intro"])
            categories = d[key]["categories"]

            for category in categories.keys():
                print(category)
                for meds in (categories[category].keys()):
                    print(meds)
                    for ms in categories[category][meds]:
                        # directory=os.getcwd()+f"\vid/{key}\categories\"
                        if category[-1] == " ":
                            directory = base_dir + r"\vid" + f"\{key[1:-2]}" + r"\categories" + f"\{category[0:-2]}" + f"\{meds}"
                        else:
                            directory = base_dir + r"\vid" + f"\{key[1:-2]}" + r"\categories" + f"\{category}" + f"\{meds}"
                        print(directory)
                        try:
                            os.chdir(directory)
                        except Exception as e:
                            print(e)
                            os.makedirs(directory)
                            os.chdir(directory)
                        down(ms)
                    print(categories[category][meds])


def down(link):
    def convert(lnk):
        ln = "https://youtu.be/" + lnk.split("?v=")[1]
        return ln

    try:
        video = pafy.new(convert(link))
        best = video.getbest()
        print(best.resolution, best.extension)
        b = best.download()
        print(b)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
