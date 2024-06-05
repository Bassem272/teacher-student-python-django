import datetime
from telnetlib import STATUS
from django.shortcuts import render
from django.urls import reverse
from grpc import Status
import jwt
from requests import Response
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse

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

from django.http import JsonResponse, HttpResponseBadRequest
# from .email_code import send_verification_code_email
from firebase_admin import firestore
from django.contrib.auth.hashers import make_password

from django.http import HttpResponseNotFound

from django.core.validators import MaxLengthValidator, EmailValidator
from django.core.exceptions import ValidationError

from firestore_utils import get_firestore_client

# Connection to the firestore
db = get_firestore_client()


# Create your views here.

import uuid


# Function to get the next message ID
def get_next_article_id():
    return f'--article_{uuid.uuid4()}'

@api_view(["POST"])
def create_article(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)

    if not data:
        return JsonResponse({'message': 'Request body is empty'}, status=400)

    content = data.get('content')
    if not content:
        return JsonResponse({"message": 'Message content is required'}, status=400)
    
    userEmail = data.get('email')
    if not userEmail:
        return JsonResponse({"message": "User email is required"}, status=400)
    author = data.get('author')
    if not  author:
        return JsonResponse({"message": "author is required"}, status=400)
    title = data.get('title')
    if not  title:
        return JsonResponse({"message": "title is required"}, status=400)

    email_validator = EmailValidator()
    try:
        email_validator(userEmail)
    except ValidationError:
        return JsonResponse({"message": "Invalid email format"}, status=400)

    grade = data.get('grade')
    if not grade:
        return JsonResponse({"message": "Grade is required"}, status=400)
    chat_grade_doc_ref = db.collection('chat').document(grade).get()
    chat_grade_doc = chat_grade_doc_ref.to_dict()
    article_id = get_next_article_id()

    print(article_id)
    article = {article_id: {
        'email': userEmail,
        'content': content,
        'author': author,
        'grade': grade,
        'title':title,
        'timeStamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    }
    try:

        articles_doc_ref = db.collection('articles').document(grade)
        
        articles_doc = articles_doc_ref.get()
        if articles_doc.exists:
            articles_doc_ref.set(article, merge=True)

            articles_doc_ref = db.collection('articles').document(grade)
            articles_doc_dict = articles_doc_ref.get().to_dict()
            lista = list(articles_doc_dict.items())
            print(lista)
            last_article_id = list(articles_doc_dict.keys())[-1]
            articles_doc_ref.set(article, merge=True)
            return JsonResponse({"article": "article added to the chat successfully",
                                    "last_article_id": last_article_id,
                                    "chat_grade_doc": articles_doc.to_dict(),
                                 }, status=201)
        else:
            return JsonResponse({"message": "Could not find the article document"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


@api_view(['delete'])
def delete_article(request, id):
    try: 
        data = json.loads(request.body)
        if(not data):
            return HttpResponseBadRequest('the body is empty') 
        if( not id): 
            return HttpResponseBadRequest("article id is not provided")
        grade = data.get('grade')
        if not grade:
            return JsonResponse({"message": "Grade is required"}, status=400)
        try:
            articles_doc_ref = db.collection('articles').document(grade)
            articles_doc_dict = articles_doc_ref.get().to_dict()
            articles_doc_list = list(articles_doc_dict.keys())
            if(id not in articles_doc_list):
                return JsonResponse({"message": "article not found"}, status=404)
            else:
                articles_doc_ref.update({id: firestore.DELETE_FIELD})
                return JsonResponse({"message": "article deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@api_view(['put'])    
def update_article(request,id):
    try:
        data = json.loads(request.body)
        if(not data):
            return HttpResponseBadRequest('the body is empty') 
        if( not id): 
            return HttpResponseBadRequest("article id is not provided")
        grade = data.get('grade')
        if not grade:
            return JsonResponse({"message": "Grade is required"}, status=400)
        content = data.get('content')
        if not content:
            return JsonResponse({"message": "Content is required"}, status=400)
        userEmail = data.get('email')
        if not userEmail:
            return JsonResponse({"message": "User email is required"}, status=400)
        author = data.get('author')
        if not  author:
            return JsonResponse({"message": "author is required"}, status=400)
        title = data.get('title')
        if not  title:
            return JsonResponse({"message": "title is required"}, status=400)
        try:
            articles_doc_ref = db.collection('articles').document(grade)
            articles_doc = db.collection('articles').document(grade).get()
            articles_doc_dict = articles_doc.to_dict()
            articles_doc_list = list(articles_doc_dict.keys())
            print(articles_doc_list)
            print(id)
            if(id not in articles_doc_list):
                return JsonResponse({"message": "Message not found"}, status=404)
            else:
                articles_doc_ref.update({id:{
                        'email': userEmail,
                        'content': content,
                        'author': author,
                        'grade': grade,
                        'title':title,
                        'timeStamp': datetime.datetime.now(datetime.timezone.utc).isoformat()

                }})
                return JsonResponse({ 
                    "message": "article updated successfully",

                                        "edited article": {id:{
                        'email': userEmail,
                        'content': content,
                        'author': author,
                        'grade': grade,
                        'title':title,
                        'timeStamp': datetime.datetime.now(datetime.timezone.utc).isoformat()

                }}
                                        }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['get'])
def get_all_articles(request):
    try:
        data = json.loads(request.body)
        if(not data):
            return HttpResponseBadRequest('the body is empty') 
        grade = data.get('grade')
        if not grade:
            return JsonResponse({"message": "Grade is required"}, status=400)
        try:
            articles_doc_ref = db.collection('articles').document(grade).get()
            articles_doc_dict = articles_doc_ref.to_dict()
            articles_doc_list = list(articles_doc_dict.items())
            return JsonResponse({"message": "articles fetched successfully",
                
                                        "articles": articles_doc_list
                                            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)    



@api_view(['delete'])
def delete_all_articles(request):
    try:
        data = json.loads(request.body)
        if(not data):
            return HttpResponseBadRequest('the body is empty')
        grade = data.get('grade')
        if not grade:
            return JsonResponse({"message": "Grade is required"}, status=400)
        try:
            chat_doc_ref = db.collection('articles').document(grade)
            chat_doc_ref.set({},merge=False)
            return JsonResponse({"message": "articles deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
