import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, physcologist, institution, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault("paid", True)
        other_fields.setdefault("unique", email)
        other_fields.setdefault("ratingd", 0)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, physcologist, institution, **other_fields)

    def create_user(self, email, user_name, first_name, password, physcologist, institution, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        if not physcologist:
            institution = "blank"

        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, physcologist=physcologist, institution=institution, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, )
    unique = models.CharField(max_length=150, default=email, unique=True)
    # user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    institution = models.CharField(max_length=150, blank=True)
    physcologist = models.BooleanField(default=False)

    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    ratings = models.FloatField(default=2.5)
    # range of 0 to 5
    # physcologist and your personal health

    is_active = models.BooleanField(default=False)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', "first_name", "institution", "physcologist"]

    def __str__(self):
        return self.user_name


"""
class Physcological_session(models.Model):
    p = f"{settings.MEDIA_ROOT}/sessions/{uuid}"
    symptoms = models.FilePathField(path=f"{p}/symptoms.json")
    diagnosis = models.FilePathField(path=f"{p}/diagnosis.json")
    story = models.FilePathField(path=f"{p}/story.txt")
    feelings = models.FilePathField(path=f"{p}/feelings.csv")
 p = f"{settings.MEDIA_ROOT}/userdata"
    os.makedirs(p, exist_ok=True)
    tg = models.FilePathField(path=p + f"/tg/{unique}.json")
    physcological_sessions = models.FilePathField(path=p + f"/ps/{unique}.json")

"""


class Psychological_Session(models.Model):
    time_start = models.DateTimeField(default=timezone.now)
    symptoms = models.CharField(max_length=1500)  # to file
    diagnosis = models.CharField(max_length=150, )
    story = models.CharField(max_length=150, )
    feelings = models.CharField(max_length=150, )
    link = models.CharField(max_length=150, )
    psychologist = models.CharField(max_length=150, )
    # user_id
    counselee = models.CharField(max_length=150)
    storage_id_sessions = models.CharField(max_length=150, )
    in_session = models.BooleanField(default=True)


class Post(models.Model):
    user = models.CharField(max_length=150)
    path = models.CharField(unique=True, max_length=150)
    likes = models.IntegerField()
    views = models.IntegerField()
