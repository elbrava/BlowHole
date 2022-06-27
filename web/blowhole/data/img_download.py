import threading
from time import sleep

import english_words
import validators
from bs4 import *
import requests
import os

from nltk import word_tokenize
from nltk.corpus import stopwords

count = 1
base_dir = os.getcwd()
import lxml
from bs4 import BeautifulSoup
import json

link_dict = {}


def mainner():
    with open("json/motiv.json", "r") as f:
        d = dict(json.load(f))
        for key in d.keys():
            que = key
            for l in d[que]["intro"]:
                directory = base_dir + r"\shorts" + f"\{key[1:-2]}" + "\intro"
                try:
                    t = threading.Thread(target=main, args=[l, directory])

                    t.start()
                except:
                    pass
            for title in (d[key]["categories"]).keys():
                for li in (d[key]["categories"][title]):
                    if title[-1] == " ":
                        directory = base_dir + r"\shorts" + f"\{key[1:-2]}" + r"\categories" + f"\{title[0:-2]}"
                    else:
                        directory = base_dir + r"\shorts" + f"\{key[1:-2]}" + r"\categories" + f"\{title}"
                    try:
                        t = threading.Thread(target=main, args=[li, directory])

                        t.start()
                    except:
                        pass


# first we will search for "data-srcset" in img tag
def folder_create(name, folder_name):
    global count
    f = folder_name
    folder_name += f"\{name}"
    folder_name = r"{}".format(folder_name)
    if (not os.path.isdir(folder_name)) or name == "":
        name = r"{}".format(count)
        folder_name = f"{f}\{name}"
        folder_name = r"{}".format(folder_name)
        count += 1

    try:
        # folder creation
        os.makedirs(r"{}".format(folder_name))

    # if folder exists with that name, ask another name
    except OSError as e:
        pass
    return name


def loop_image(image, path, url):
    global count
    folder_name = path
    count = 0
    li = ""
    image_link = ""
    try:
        # In image tag ,searching for "data-srcset"
        image_link = image["data-srcset"]

    # then we will search for "data-src" in img
    # tag and so on..
    except:
        try:
            # In image tag ,searching for "data-src"
            image_link = image["data-src"]
        except:
            try:
                # In image tag ,searching for "data-fallback-src"
                image_link = image["data-fallback-src"]
            except:
                try:
                    # In image tag ,searching for "src"
                    image_link = image["src"]

                # if no Source URL found
                except:
                    pass
    # From image tag ,Fetch image Source URL

    # 1.data-srcset
    # 2.data-src
    # 3.data-fallback-src
    # 4.src

    # Here we will use exception handling
    if not validators.url(image_link):
        image_link = url + image_link
    try:
        name = image["alt"]
    except:
        li = image_link.split("://")[1]

        name = r"{}".format(count)
        count += 1
    # After getting Image Source URL
    # We will try to get the content of image
    try:

        r = requests.get(image_link).content

        try:

            # possibility of decode
            r = str(r, 'utf-8')


        except UnicodeDecodeError:

            # After checking above condition, Image Download start
            name = folder_create(name, folder_name)
            folder_name = folder_name + f"\{name}"
            if len(os.listdir()) != 2:

                try:

                    with open(f"{folder_name}\{name}.jpg", "wb+") as f:
                        f.write(r)
                        f.close()
                    f = r"\{}".format(name)

                    th = threading.Thread(target=img_recog, args=[f"{folder_name + f}.jpg"])
                    th.start()
                except OSError:
                    sleep(4)
                    with open(f"{folder_name}\{name}.jpg", "wb+") as f:
                        f.write(r)
                        f.close()
                    th = threading.Thread(target=img_recog, args=[f"{folder_name}\{name}.jpg"])
                    th.start()
            else:
                print(folder_name)
    except Exception as e:
        print(e)

    # There might be possible, that all
    # images not download
    # if all images download
    else:
        pass


# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name, url):
    # initial count is zero
    count = 0
    path = folder_name
    # print total images found in URL

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            th = threading.Thread(target=loop_image, args=[image, path, url])
            th.start()


# MAIN FUNCTION START
def main(url, path):
    # content of URL
    r = requests.get(url)

    # Parse HTML Code
    soup = BeautifulSoup(r.text, 'html.parser')

    # find all images in URL
    images = soup.findAll('img')

    # Call folder create function
    download_images(images, path, url)


import pathlib


def img_recog(path):
    print(path)
    # Import required packages
    import cv2
    import pytesseract
    try:
        # Mention the installed location of Tesseract-OCR in your syste
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        # Read image from which text needs to be extracted
        img = cv2.imread(path)

        # Preprocessing the image starts

        # Convert the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        # Specify structure shape and kernel size.
        # Kernel size increases or decreases the area
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)

        # Creating a copy of image
        im2 = img.copy()

        # A text file is created and flushed
        file = open(path + "recognized.txt", "w+")
        file.write("")
        file.close()
        file_text = ""
        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        orig = path + "recognized.txt"
        with  open(path + "recognized.txt", "a+") as file:
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)

                # Drawing a rectangle on copied image
                rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Cropping the text block for giving input to OCR
                cropped = im2[y:y + h, x:x + w]

                # Open the file in append mode

                # Apply OCR on the cropped image
                text = pytesseract.image_to_string(cropped)

                # Appending the text into file
                file.write(text)
                file_text += text
                file.write("\n")
                file_text += "\n"

            path = pathlib.Path(path).parent.absolute()
            main_sentence(file_text)
            # text_speech.sound_get(file_text, path)
    except OSError:
        sleep(4)
        # text_speech.sound_get(file_text, path)
        th = threading.Thread(target=img_recog, args=path)
        th.start()


mainner()


def main_sentence(words):
    print(words)
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
