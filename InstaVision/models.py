from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
import pandas as pd


# Create your models here.


class UserTokens(models.Model):
    """
    # This model contains all the user tokens till the browser is closed.
    """
    key = models.CharField(unique=True,max_length=20)
    def create(key):
        usertoken = UserTokens()
        usertoken.key = key
        usertoken.save()
        return usertoken

class ImagesFile(models.Model):
    """
    # Contains all the image files mapped to the user token
    """

    key = models.ForeignKey(UserTokens, on_delete=models.CASCADE)
    images_file_name = models.CharField(max_length=25)
    file = models.TextField()

    def create(key = None, name = '', file = None):
        imgs_file = ImagesFile()
        imgs_file.key = key
        imgs_file.images_file_name = name
        imgs_file.file = file
        imgs_file.save()
        return imgs_file


class CommentsFile(models.Model):
    """
    # Contains all the comments files mapped to the user token
    """

    key = models.ForeignKey(UserTokens,on_delete=models.CASCADE)
    comments_file_name = models.CharField(max_length=25)
    file = models.TextField()
    def create(key=None, name='', file=None):
        comments_file = CommentsFile()
        comments_file.key = key
        comments_file.comments_file_name = name
        comments_file.file = file
        comments_file.save()
        return comments_file


class InstaVisionModel(models.Model):
    """
    # The main table which contains all the data of each request.
    """
    key = models.ForeignKey(UserTokens,on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, auto_created=True)
    page_url = models.CharField(max_length=300)
    max_posts = models.IntegerField()
    images_file = models.ForeignKey(ImagesFile, on_delete=models.CASCADE)
    comments_file = models.ForeignKey(CommentsFile, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)


    def create( page_url = "", max_posts = 0, key = '', images_file = None, comments_file = None):
        insta_vision_model = InstaVisionModel()
        insta_vision_model.page_url = page_url
        insta_vision_model.max_posts = max_posts
        insta_vision_model.images_file = images_file
        insta_vision_model.key = key
        insta_vision_model.comments_file = comments_file
        insta_vision_model.save()
        return insta_vision_model

