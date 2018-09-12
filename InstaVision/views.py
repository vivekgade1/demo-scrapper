from django.http import HttpResponse, JsonResponse
from django.http import Http404
import pandas as pd
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.middleware.csrf import _get_new_csrf_token
from requests import HTTPError
from django.core import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json

from InstaVision.models import InstaVisionModel, UserTokens, CommentsFile, ImagesFile
from InstaVision.serializer import InstaVisionSerializer
from InstagramScrapper.utils.response import ResponseModelJson, ResponseModelXl, ResponseModelCsv
from MetricLibs.instagram_scraper import InstagramScrapper

@csrf_protect
def get_insta_data(request):
    try:
        user_key = request.environ.get('HTTP_X_CSRFTOKEN')
        request_params = request.GET.dict()
        request_params['max_posts'] = int(request_params['max_posts'])
        user_token_obj = UserTokens.objects.get(key= user_key)
        (comments_df, images_df) = InstagramScrapper(**request_params).crawler_init()
        # comments_df = pd.read_excel('C:/Users/Akshith/Documents/Vivek/InstagramScrapper/comment_vgade.xlsx')
        # images_df = pd.read_excel('C:/Users/Akshith/Documents/Vivek/InstagramScrapper/image_vgade.xlsx')
        comments_obj = CommentsFile.create(key = user_token_obj, name= request_params['comments_file'], file= comments_df.to_csv())
        images_obj = ImagesFile.create(key = user_token_obj, name= request_params['images_file'], file= images_df.to_csv())
        request_model = InstaVisionModel.create(
                                key = user_token_obj,
                                page_url = request_params.get('page_url'),
                                max_posts = request_params.get('max_posts'),
                                comments_file = comments_obj,
                                images_file = images_obj
                                )
        return ResponseModelJson.success(
            data=InstaVisionSerializer(InstaVisionModel.objects.filter(key=user_token_obj), many=True).data)

    except Exception as err:
        raise err

@csrf_exempt
def get_auth_token(request):
    new_auth_token = _get_new_csrf_token()
    new_user = UserTokens.create(new_auth_token)
    return ResponseModelJson.success(auth_tok = new_user.key)

@csrf_protect
def get_comments_file(request):
    request_params = request.GET.dict()
    comments_obj = CommentsFile.objects.get(id = request_params['id'])
    return ResponseModelCsv(file= comments_obj.file, name = comments_obj.comments_file_name)

@csrf_protect
def get_images_file(request):
    request_params = request.GET.dict()
    images_obj = ImagesFile.objects.get(id = request_params['id'])
    return ResponseModelCsv(file= images_obj.file, name= images_obj.images_file_name)

@csrf_protect
def get_all_requests(request):
    try:
        user_key = request.environ.get('HTTP_X_CSRFTOKEN')
        request_params = request.GET.dict()
        user_token_obj = UserTokens.objects.get(key=user_key)
        return ResponseModelJson.success(
            data= InstaVisionSerializer(InstaVisionModel.objects.filter(key=user_token_obj),many=True).data)
    except Exception as err:
        raise err
