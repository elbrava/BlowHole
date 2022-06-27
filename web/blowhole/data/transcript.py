import threading

import english_words
from nltk import word_tokenize
from nltk.corpus import stopwords
from youtube_transcript_api import YouTubeTranscriptApi
import json

d = {"tags": []}
with open("json/tags.json", "w") as f:
    json.dump(d, f)
    f.close()
print(d)

link_dict = {}


def transcribe(id):
    video_id = id
    tl = YouTubeTranscriptApi.get_transcript(video_id)
    print(len(tl))
    if tl:
        for m in tl:
            main_sentence(m["text"])

    return tl


def main():
    dict_all = {}
    with open("json/video.json", "r") as f:
        d = dict(json.load(f))
        for key in d.keys():
            query = key
            print(key)
            # intro
            intro_list = d[key]["intro"]
            for intro in intro_list:
                print(intro)
                try:
                    id = intro.split("?v=")[-1]
                    t = transcribe(id)
                    if t is None:
                        raise ValueError

                except:
                    continue
                else:
                    link_dict[key] = {}
                    link_dict[key]["intro"] = {}
                    link_dict[key]["intro"][id] = t

            categories = d[key]["categories"]

            for category in categories.keys():
                print(category)
                for meds in (categories[category].keys()):
                    print(meds)
                    for ms in categories[category][meds]:
                        try:
                            id = ms.split("?v=")[-1]
                            t = transcribe(id)
                            if t is None:
                                raise ValueError
                        except:
                            continue
                        else:
                            link_dict[key] = {}
                            link_dict[key]["categories"] = {}
                            link_dict[key]["categories"][category] = {}
                            link_dict[key]["categories"][category][meds] = {}
                            link_dict[key]["categories"][category][meds][id] = t

    with open("json/transcript.json", "w+") as f:
        json.dump(link_dict, f)


def main_sentence(words):
    num = word_tokenize(words)

    for word in num:

        main_word(word)


def main_word(word):
    word = r"{}".format(word.strip())
    with open(r"json/tags.json", "r") as f:

        tags_dict = dict(json.load(f))
        tags = tags_dict["tags"]
        if word in english_words.english_words_set:
            if word not in stopwords.words('english'):
                tags.append(word)
        f.close()
        with open(r"json/tags.json", "w+") as g:
            json.dump(tags_dict, g)
            f.close()


if __name__ == '__main__':
    main()
