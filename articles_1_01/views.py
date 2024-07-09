import json
from django.shortcuts import render
import datetime
from telnetlib import STATUS
from django.shortcuts import render
from django.urls import reverse
from grpc import Status
import jwt
from requests import Response
import json
from firebase_admin import auth
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
import random
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound,  HttpResponse, HttpResponseForbidden
# from .email_code import send_verification_code_email
from firebase_admin import firestore
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
import threading
import uuid
from firestore_utils import get_firestore_client
import logging

logger = logging.getLogger(__name__)
# Connection to the firestore
db = get_firestore_client()
# Create your views here.
# {
#   "id": "article1",
#   "title": "Teaching at XYZ School",
#   "author": "John Doe",
#   "date": "2024-06-01",
#   "tags": ["education", "teaching"],
#   "content": [
#     {
#       "type": "paragraph",
#       "content": "Teaching at XYZ School has been a wonderful experience..."
#     },
#     {
#       "type": "image",
#       "url": "https://example.com/image.jpg",
#       "caption": "XYZ School"
#     },
#     {
#       "type": "paragraph",
#       "content": "The students are very enthusiastic and eager to learn..."
#     }
#   ]
# }


@api_view(["POST"])
def create_article(request):
    data = json.loads(request.body)
    subject = data.get("subject")
    grade = data.get("grade")
    title = data.get("title")
    author = data.get("author")
    date = data.get("date")
    content = data.get("content")
    tags = data.get("tags")

    if not title or not author or not date or not content or not tags:
        return HttpResponseBadRequest("Missing required fields")

    # Generate a unique article ID with a prefix
    article_id = f"article_{uuid.uuid4()}"
    article_data = {
        "id": article_id,
        "author": author,
        "title": title,
        "date": datetime.datetime.now(),
        "content": content,
        "tags": tags,
    }
    try:
        # db.collection('levels').document(grade).set(article_data)
        db.collection('levels').document(grade).collection('subjects').document(subject).collection('articles').document(article_id).set(article_data)
        return JsonResponse(
            {"message": "article created successfully", "article_data": article_data},
            status=201,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    # data = json.loads(request.body)
    # print(data)
    # return Response({"message": "Hello, World! from articles!"})


@api_view(["POST"])
def create_article_g(request , grade, subject):
    data = json.loads(request.body)
    # subject = data.get("subject")
    # grade = data.get("grade")
    title = data.get("title")
    author = data.get("author")
    date = data.get("date")
    content = data.get("content")
    tags = data.get("tags")
    subject = data.get("subject")
    grade = data.get("grade")

    if not title or not author or not date or not content or not tags or not subject or not grade:
        return HttpResponseBadRequest("Missing required fields")

    # Generate a unique article ID with a prefix
    article_id = f"article_{uuid.uuid4()}"
    article_data = {
        "id": article_id,
        "author": author,
        "title": title,
        "date": datetime.datetime.now(),
        "content": content,
        "tags": tags,
        'subject':subject,
        "grade": grade
    }
    try:
        # db.collection('levels').document(grade).set(article_data)
        db.collection('levels').document(grade).collection('subjects').document(subject).collection('articles').document(article_id).set(article_data)
        return JsonResponse(
            {"message": "article created successfully", "article_data": article_data},
            status=201,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    # data = json.loads(request.body)
    # print(data)
    # return Response({"message": "Hello, World! from articles!"})

from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt

# @api_view(["POST"])
# def create_article(request):
#     data = json.loads(request.body)
#     print(data)
#     title = data.get("title")
#     author = data.get("author")
#     date = data.get("date")
#     content = data.get("content")
    
#     tags = data.get("tags")
#     if not author or not title  or not content or date or not tags:
#         return HttpResponseBadRequest("Missing required fields")

#     # Generate a unique article ID with a prefix
#     article_id = f"article_{uuid.uuid4()}"
#     article_data = {
#         "id": article_id,
#         "author": author,
#         "title": title,
#         "date": date,
#         "content": content,
#         "tags": tags,
        
#     }
#     try:
#         db.collection('articles').document(article_id).set(article_data)
#         return JsonResponse(
#             {"message": "article created successfully", "article_data": article_data},
#             status=201,
#         )
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
def get_article(request,  article_id):
    logger.info(f"get_article is here: { article_id}")
    try:
        doc_ref = db.collection('articles').document(article_id)
        doc = doc_ref.get()
        if doc.exists:
            article_data = doc.to_dict()
            logger.info(f"article found: {article_data}")
            return JsonResponse({"article_data": article_data}, status=200)
        else:
            return JsonResponse({"error": "article not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(["GET"])    
def get_all_articles(request):
    try:
        articles = []
        docs = db.collection('articles').get()
        for doc in docs:
            article_data = doc.to_dict()
            articles.append(article_data)
            
        return JsonResponse({"articles": articles}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# authentication/views.py

@api_view(["GET"])
def get_grades(request):
    try:
        levels_ref = db.collection('levels')
        grades = [doc.id for doc in levels_ref.stream()]
        return JsonResponse({"grades": grades}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
# authentication/views.py

@api_view(["GET"])
def get_subjects(request, grade):
    try:
        subjects_ref = db.collection('levels').document(grade).collection('subjects')
        subjects = [doc.id for doc in subjects_ref.stream()]
        return JsonResponse({"subjects": subjects}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
# authentication/views.py

@api_view(["GET"])
def get_articles(request, grade, subject):
    try:
        articles_ref = db.collection('levels').document(grade).collection('subjects').document(subject).collection('articles').get()
        articles = []
        for doc in articles_ref:
            article_data = doc.to_dict()
            articles.append(article_data) 
        # articles = [doc.title for doc in articles_ref.stream()]
        return JsonResponse({"articles": articles}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
# authentication/views.py

@api_view(["GET"])
def get_article(request, grade, subject, article_id):
    try:
        article_ref = db.collection('levels').document(grade).collection('subjects').document(subject).collection('articles').document(article_id)
        article = article_ref.get()
        if article.exists:
            return JsonResponse({"article": article.to_dict()}, status=200)
        else:
            return JsonResponse({"error": "Article not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def recommended_articles(request, grade):
    try:
        docs = db.collection('levels').document(grade).collection('subjects')
        subjects = [doc.id for doc in docs.stream()]
        recommended_articles = []
        for subject in subjects: 
            articles = db.collection('levels').document(grade).collection('subjects').document(subject).collection('articles')
            articles_arr = [doc.to_dict() for doc in articles.stream()]
            
            recommended_articles.extend(articles_arr)
        # all_articles = [article for articles in recommended_articles.values() for article in articles]
         # Shuffle the list and get 6 random articles
        # random.shuffle(all_articles)
         # Shuffle the list and get 6 random articles
        random.shuffle(recommended_articles)
        # print("arti",articles_arr)
        flattened_articles = recommended_articles[:6] 
        # print("recommended",flattened_articles)
   
        return JsonResponse({'recommended_articles':flattened_articles}, status=200)
    except Exception as e : 
        return JsonResponse({"error" : str(e) }, status= 500 )        