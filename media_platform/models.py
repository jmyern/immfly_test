from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from media_platform.utils.languages import LANGUAGE_LIST
import os


class ContentMetadata(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()
    content = models.ForeignKey('Content', on_delete=models.CASCADE)


class ContentFile(models.Model):
    # upload_to path will be changed on insert with a reference to the channel
    media_file = models.FileField(upload_to=os.path.join("media_platform", "content"))
    content = models.ForeignKey('Content', on_delete=models.CASCADE)


class Content(models.Model):
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )


class Channel(models.Model):
    title = models.CharField(max_length=255)
    language = models.IntegerField(choices=LANGUAGE_LIST)
    picture = models.FileField(upload_to=os.path.join("media_platform", "picture"))
    sub_channels = models.ManyToManyField('Channel')
    content = models.ManyToManyField('Content')
