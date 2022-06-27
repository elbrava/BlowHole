import hashlib
import json
import os
import pathlib
import random
import threading
import time
from functools import partial
from string import Template

import pandas as pd
from agora_token_builder import RtcTokenBuilder
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from firebase_admin import db

from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives

from .models import *

name = ""


def home(request):
    print(settings.BASE_DIR)
    return render(request, "index.html")


def getToken(request):
    appId = "e833666842c944769de26a864e6af2e6"
    appCertificate = "2ff2339c7c674e9eb0f3ddc36f66d1f2"
    counselee = request.user.id
    psychologist = request.GET["psychologist"]
    p = Psychological_Session()
    channelName = hashlib.pbkdf2_hmac(
        'sha256', psychologist.encode(), counselee.encode(), 7777).hex()
    p.counselee = counselee
    p.psychologist = psychologist
    p.link = channelName
    p.save()

    # counselee
    # physcologist
    # save
    # link
    # tel both users they are in session via email

    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    # render it to page for email
    return JsonResponse({'token': token, 'uid': uid}, safe=False)


def unique_img(request):
    weights = random.randint(2, 3)
    print(weights)
    x = random.randint(0, 14)
    ty_pe = os.listdir(settings.MEDIA_ROOT + '/shorts')[x]
    path = f"shorts/{ty_pe}"

    na_me = ''
    if weights == 3:
        p = settings.MEDIA_ROOT + "/" + path + "/categories"
        l = os.listdir(p)
        y = random.randint(0, len(l))
        subtype = l[y]
        path = p + f"/{subtype}"
        l = os.listdir(path)
        y = random.randint(0, len(l))
        path = path + f"/{l[y]}"
        path = path + f"/{os.listdir(path)[0]}"
        print(path)

        return HttpResponse(ty_pe + " -+-  " + subtype + " |" + path)

    if weights == 2:
        p = settings.MEDIA_ROOT + "/" + path + "/intro"
        l = os.listdir(p)
        y = random.randint(0, len(l))
        path = path + f"/intro/{l[y]}"
        print(path)
        na_me = ty_pe
        return HttpResponse(na_me + " |" + path)


def video(request):
    with open(f"{settings.MEDIA_ROOT}/json/video.json", "r") as f:
        weights = 3
        print(weights)
        d = dict(json.load(f))
        x = random.randint(0, len(d.keys()) - 1)
        ty_pe = d[list(d.keys())[x]]
        if weights == 2:
            t = ty_pe["intro"]
            y = random.randint(0, len(t) - 1)
            vid = t[y]
            return HttpResponse(vid)
        if weights == 3:
            t = ty_pe["categories"]
            try:
                x = random.randint(0, len(t.keys()) - 1)
                sub_type = t[list(t.keys())[x]]
                x = random.randint(0, len(sub_type.keys()) - 1)
                sub_sub_type = sub_type[list(sub_type.keys())[x]]
                y = random.randint(0, len(sub_sub_type) - 1)
                vid = sub_sub_type[y]
                return HttpResponse(vid)
            except:
                return video(request)


def talk(request, channel_name):
    pass


def token_gen(request):
    pass


def post_content(request):
    f = request.FILES["POST"]
    p = Post()
    p.user = request.user.unique
    p.path = settings.MEDIA_URL + "/user_vid/{p.pk}"
    fs = FileSystemStorage(location=settings.MEDIA_ROOT + f"/user_vid/{p.pk}")
    fs.save(f.name, f)
    p.views = 1
    p.likes = 1
    p.save()


# randomized
def get_content(request):
    p = Post.objects.all()
    p = p[random.randint(0, len(p) - 1)]
    path = settings.MEDIA_ROOT + f"/user_vid/{p.pk}"
    path = os.listdir(path)[0]

    path = settings.MEDIA_URL + f"/user_vid/{p.pk}/{path}"
    return HttpResponse(path)


def signup(request):
    global name
    if request.method == "GET":
        return render(request, r"signup.html", {})
    else:
        print("no prob")
        dict_signup = dict(request.POST)
        print(dict_signup)

        institution = dict_signup['INSTITUTION'][0]
        course = dict_signup['COURSE'][0]
        username = dict_signup['USERNAME'][0]
        group = dict_signup['GROUP'][0]
        email = dict_signup['EMAIL'][0]
        print(email)
        email = str(email)
        if email.__contains__("."):
            name = email
            first_name = email.split()[0]
        else:
            first_name = email.split("@")[0]
        password1 = hashlib.pbkdf2_hmac(
            'sha256', email.encode(), dict_signup["PASS1"][0].encode(), 7777).hex()
        password2 = hashlib.pbkdf2_hmac(
            'sha256', email.encode(), dict_signup["PASSWORD2"][0].encode(), 7777).hex()

        if not password1 == password2:
            messages.info(request, "PASSWORD MISMATCH")
            return render(request, r"signup.html",
                          {"INSTITUTION": institution[0], "COURSE": course[0], "GROUP": group[0], "EMAIL": email,
                           "PASS1": "",
                           "PASSWORD2": ""})
        else:
            print(password1, password2)
            try:
                User = get_user_model()
                if group:
                    user = User.objects.create_user(user_name=username, first_name=name, institution=institution,
                                                    group=group, course=course, email=email,
                                                    password=password1, unique=password1)
                else:
                    user = User.objects.create_user(user_name=username, first_name=name, institution=institution,
                                                    course=course, email=email,
                                                    password=password1, unique=password1)
                user.set_password(password1)
                user.save()

                link_verification = settings.SERVER + f"/user/activate/{user.unique}"
                # link_verification="https://sustainability.google/commitments/?utm_source=googlehpfooter&utm_medium=housepromos&utm_campaign=bottom-footer&utm_content="
                print(link_verification)
                t = threading.Thread(target=partial(
                    sendmail, request, email, link_verification))
                t.start()

            except Exception as e:
                print(e)
                messages.info(request, "USERNAME ALREADY EXISTS")
                return render(request, r"signup.html",
                              {"INSTITUTION": "", "COURSE": "", "GROUP": "", "EMAIL": "", "PASS1": "", "PASSWORD2": ""})
            else:
                ref = db.reference('/')

                with open(f'{settings.BASE_DIR}' + r'\main.json', "r") as store:
                    data = json.load(store)
                    temp = {password1: {
                        "name": name,
                        "university": institution[0],
                        "course": course[0],
                        "group": group[0],
                        "student_email": email,
                        "socials": [],
                        "units": [],
                        "notes": {},
                        "records": {}

                    }
                    }
                    data[password1] = temp[password1]
                    ref.child("root").set(temp)
                    with open(f'{settings.BASE_DIR}' + r'\main.json', "w") as store:
                        json.dump(data, store)

                    messages.info(
                        request, "LOGIN TO YOUR SUCCESSFULLY CREATED AN ACCOUNT")
                    return render(request, r"login.html", {name: name})


def test(request):
    global v
    v += 1
    return render(request, r"test.html", {"counter": v})
    # email validation
    # internet error
    # fireBase


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.info(request, "Successfully logged out")
        return render(request, "login.html")
    else:
        return render(request, "login.html")


# Create your views here.
def profile(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            file_path = f"{settings.BASE_DIR}" + r"\records" + f"\{user.unique}.csv"
            p = pd.read_csv(file_path)
            print(p.iloc[0])
            v = len(p.values)

            units = []
            units_test = []
            record_urls = []
            notes_urls = []
            for pk in range(v):
                p = p.iloc[int(pk)]
                if not (units_test.__contains__(p.unit)):
                    units_test.append(p.unit)
                    units.append([p.unit, [p.topic]])
                else:
                    if not units[units.index(p.unit)][1].__contains__(p.topic):
                        units[units.index(p.unit)][1].append(p.topic)

                url = str(p.files).split(r"C:\Users\Admin\Desktop\SOMA\records")[-1]

                try:
                    s = open(str(p.files) + r"\record.html")
                except Exception as e:
                    edited = "Not Edited"
                else:
                    edited = "edited"
                record_urls.append(
                    [p.unit, p.topic, p.day, edited, request._current_scheme_host + "/media" + url + r"/record.wav"])
                notes_urls.append(
                    [p.unit, p.topic, p.day, request._current_scheme_host + f"/user/notes/{pk}"])

            return render(request, r"profile.html", {"records": record_urls, "notes": notes_urls, "units": units})

        else:

            return render(request, r"login.html", {"redirect": "profile"})
    else:
        user = request.user
        print("no prob")
        dict_signup = dict(request.POST)
        print(dict_signup)

        institution = dict_signup['INSTITUTION'][0]
        course = dict_signup['COURSE'][0]
        username = dict_signup['USERNAME'][0]
        group = dict_signup['GROUP'][0]
        email = dict_signup['EMAIL'][0]
        print(email)
        email = str(email)
        if email.__contains__("."):
            name = email
            first_name = email.split()[0]
        else:
            first_name = email.split("@")[0]
        password1 = hashlib.pbkdf2_hmac(
            'sha256', email.encode(), dict_signup["PASS1"][0].encode(), 7777).hex()
        password2 = hashlib.pbkdf2_hmac(
            'sha256', email.encode(), dict_signup["PASSWORD2"][0].encode(), 7777).hex()

        if not password1 == password2:
            messages.info(request, "PASSWORD MISMATCH")
            return render(request, r"signup.html",
                          {"INSTITUTION": institution[0], "COURSE": course[0], "GROUP": group[0], "EMAIL": email,
                           "PASS1": "",
                           "PASSWORD2": ""})
        else:
            print(password1, password2)

            user.user_name = username
            user.first_name = first_name
            user.institution = institution
            user.group = group
            user.course = course
            user.email = email
            user.unique = password1
            user.set_password(password1)
            user.save()
            ref = db.reference('/')

            with open(f'{settings.BASE_DIR}' + r'\main.json', "r") as store:
                data = json.load(store)
                temp = {password1: {
                    "name": name,
                    "university": institution[0],
                    "course": course[0],
                    "group": group[0],
                    "student_email": email,
                    "socials": [],
                    "units": [],
                    "notes": {},
                    "records": {}

                }
                }
                data[password1] = temp[password1]
                ref.child("root").set(temp)
                with open(f'{settings.BASE_DIR}' + r'\main.json', "w") as store:
                    json.dump(data, store)

                messages.info(
                    request, " SUCCESSFULLY CHANGED YOUR ACCOUNT")
                return render(request, r"login.html", {name: name})


def login(request):
    if request.method == "GET":
        return render(request, r"login.html", {})
    else:
        print("no prob")
        dict_signup = dict(request.POST)
        print(dict_signup)
        email = dict_signup['EMAIL'][0]
        print(email)
        email = str(email)
        print(dict_signup["PASS1"][0])
        password1 = hashlib.pbkdf2_hmac(
            'sha256', email.encode(), dict_signup["PASS1"][0].encode(), 7777).hex()
        print(password1)
        for u in get_user_model().objects.all():
            if u.email == email:
                if u.unique == password1:
                    user = u
                else:
                    user = None
            else:
                user = None

        if user is not None:
            auth.login(request, user)
            request.user = user
            messages.info(request, "SUCCESFULLY LOGGED IN")
            if request.POST['redirect'] is not None:
                return render(request, f"{request.POST['redirect']}.html")
            else:
                return render(request, "base.html")
        else:
            messages.info(request, "INVALID CREDENTIALS")
            return render(request, "login.html")


def reset_link_gen(request):
    if request.method == "GET":
        return render(request, "reset_link_gen.html")
    else:
        email = dict(request.POST)["EMAIL"][0]
        with open(str(settings.BASE_DIR) + r"\reset.json", "r") as f:
            f = json.load(f)
            u = get_user_model().objects.filter(email=email)
            uni = u.unique
            link = settings.SERVER + f"/user/password_reset/{uni}"
            if f["reset_links"].__contains__(email):
                messages.info("Check your email, other_wise contact Admin at the about us page")
                t = threading.Thread(target=email_send_reset, args=[request, email, link])
                t.start()
            else:
                f["reset_links"].append(email)

                t = threading.Thread(target=email_send_reset, args=[request, email, link])
                t.start()
                messages.info(request, "A reset email has been sent")
        with open(str(settings.BASE_DIR) + r"\reset.json", "w") as w:
            json.dump(f, w)
        t = threading.Thread(target=partial(
            email_send_reset, request, email, link))
        t.start()
        messages.info(request, f"Email sent to {email}")
        return render(request, "base.html")


def password_reset(request, uni):
    email = get_user_model().objects.filter(unique=uni).email
    print(email)
    found = False
    with open(str(settings.BASE_DIR) + r"\reset.json", "r") as f:
        f = json.load(f)
        email_list = f["reset_links"]
        if email in email_list:
            f["reset_links"].remove(email)
            print(True)
            u = get_user_model().objects.filter(email=email)
            u.set_password(hashlib.pbkdf2_hmac(
                'sha256', email.encode(), b"0000", 7777).hex())
            u.unique = hashlib.pbkdf2_hmac(
                'sha256', email.encode(), b"0000", 7777).hex()
            found = True
            print("changed")
            u.save()
            with open(str(settings.BASE_DIR) + r"\reset.json", "w") as w:
                json.dump(f, w)
            return render(request, "password-reset.html")

        else:
            messages.info(request, "Email cannot be reset")
            with open(str(settings.BASE_DIR) + r"\reset.json", "w") as w:
                json.dump(f, w)
            return render(request, "base.html")


def email_send_reset(request, email, link):
    t = Template("""<html lang="en">
    <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sara</title>
    <style>
        body {
            background: rgb(112, 41, 99);
        }

        div {
            color: rgb(143, 214, 156);
            text-align: center;
            font-size: 300%;
        }

        a {
            margin: 0 auto;
        }

        button {
            background: rgb(143, 214, 156);
            color: rgb(112, 41, 99);
            border: 4px solid white;
            border-radius: 49px;
            margin: 0 auto;
        }
    </style>
    </head>

    <body>
    <div>
        Click the link below <br />To rest your account  <br /> With Sara
    </div>
    <div class="button">
        <a href=$link>
            <button><h1>RESET</h1></button>
        </a>
    </div>


    </body>

    </html>

    """)

    link_verification = link
    print(email)
    message = t.substitute({"link": f"{link_verification}"})
    msg = EmailMultiAlternatives(
        'Subject',
        f"Reset your password with this link {link_verification}",
        settings.EMAIL_HOST_USER,
        [email],
    )
    msg.attach_alternative(message, "text/html")
    # Main content is now text/html
    msg.send()
    messages.info(request, "Mail successfully sent")


def record(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, r"record.html", {})
        else:
            return render(request, r"login.html", {"redirect": "login"})
    else:

        file = request.FILES["file"]

        transcribes = request.POST["transcript"]
        import datetime
        dict_signup = dict(request.POST)
        unit = dict_signup["unit"][0]
        topic = dict_signup["topic"][0]
        # unit
        # topic
        print(unit, topic)
        user = request.user
        print(user.institution)
        print(datetime.date.today())

        test_path = r"{}".format(settings.MEDIA_ROOT)
        file_path = test_path + f"\{user.institution}\{user.course + user.group}\{unit}\{str(datetime.date.today())}\{topic}\{user.unique}"
        print(file_path)
        # test_path=f"{settings.BASE_DIR}\{}\{user.course}+{user.group}{unit}{datetime.date.today()}{user.id}
        topic = dict_signup['topic'][0]
        di = {
            "unit": unit,
            "topic": topic,
            "day": datetime.date.today(),
            "files": file_path,
            "classmates": [u for u in get_user_model().objects.all() if
                           (u.institution + u.course + u.group) == (user.institution + user.course + user.group)]

        }
        test_path += f"\{user.unique}.csv"
        if os.path.exists(test_path):
            print("exists")
            p = pd.read_csv(test_path, index_col=[0])
            print(len(p.values))
            i = int(len(p.values))
            dis = pd.DataFrame(di, index=[i])
            p = pd.concat([p, dis])
            print(p.head())

            p.to_csv(test_path)
        else:
            os.makedirs(pathlib.Path(test_path).parent, exist_ok=True)
            p = pd.DataFrame(di, index=[0])
            p.to_csv(test_path)

        if not os.path.exists(file_path):
            os.makedirs(file_path)
        fss = FileSystemStorage(location=file_path)
        s = fss.save(file.name, file)
        url = fss.url(s)
        with open(file_path + r"\record.txt", "w") as f:
            f.write(transcribes)
        # threading.Thread(target=mainner, args=[transcribes, file_path, unit, topic]).start()
        # silence_based_conversion(os.path.join(file_path, "record.wav"))
        return JsonResponse({"status": url})


def activate(request, unique):
    user = get_user_model()
    found = False
    print(user.objects.all())
    for u in user.objects.all():

        if str(u.unique) == str(unique):
            print(u.is_active)
            if u.is_active:
                messages.info(request, "Account already activated")
            else:
                u.is_active = True
                print("here")
                u.save()
            found = True
            break
    if not found:
        messages.info(request, "Account not found")

        return render(request, "base.html")
    else:
        messages.info(request, "Account has been activated")
        return render(request, "base.html")


def sendmail(request, email, link):
    t = Template("""<html lang="en">
<head>
<meta charset="UTF-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Sara</title>
<style>
    body {
        background: rgb(112, 41, 99);
    }

    div {
        color: rgb(143, 214, 156);
        text-align: center;
        font-size: 300%;
    }

    a {
        margin: 0 auto;
    }

    button {
        background: rgb(143, 214, 156);
        color: rgb(112, 41, 99);
        border: 4px solid white;
        border-radius: 49px;
        margin: 0 auto;
    }
</style>
</head>

<body>
<div>
    Thank you for creating<br /> An account with Sara <br /> Click button below to activate
</div>
<div class="button">
    <a href=$link>
        <button><h1>ACTIVATE</h1></button>
    </a>
</div>


</body>

</html>

""")
    link_verification = link
    print(email)
    message = t.substitute({"link": f"{link_verification}"})
    msg = EmailMultiAlternatives(
        'Subject',
        f"Reset your password with this link {link_verification}",
        settings.EMAIL_HOST_USER,
        [email],
    )
    msg.attach_alternative(message, "text/html")
    # Main content is now text/html
    msg.send()
    messages.info(request, "Mail successfully sent")


def remove_me(request, email):
    with open(str(settings.BASE_DIR) + r"\reset.json", "r") as f:
        f = json.load(f)
        email_list = f["reset_links"]
        if email in email_list:
            email_list.remove(email)

    with open(str(settings.BASE_DIR) + r"\reset.json", "w") as w:
        json.dump(f, w)

    remove_me(request, email)
    return HttpResponse(f"Successfully removed {email}")


def attach(request):
    if request.method == "GET":
        return render(request, r"login.html", {"redirect": "attach"})
    # please place your id sent to you on telegram
    if request.method == "POST":
        p = settings.MEDIA_ROOT + f"/userdata/{request.user.unique}.json"
        tgid = request.POST["tgid"]
        if os.path.exists(p):
            with open(p, "r") as f:
                f = json.load(f)
                if f["tg"]:
                    f["tg"].append(tgid)
                else:
                    f["tg"] = [tgid]
            with open(p, "w") as w:
                json.dump(f, w)
        else:
            with open(p, "w") as w:
                f = {"tg": [tgid]}
                json.dump(f, w)
        messages.info("Successfully attached  Telegram Chat id:{tgid}")
