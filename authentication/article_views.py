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
from .email_code import send_verification_code_email
from firebase_admin import firestore
from django.contrib.auth.hashers import make_password

from django.http import HttpResponseNotFound


from firestore_utils import get_firestore_client

# Connection to the firestore
db = get_firestore_client()

# views/article_views.py

@api_view(['POST'])
def create_article(request):
    data = request.data

    # Validate required fields
    required_fields = ['title', 'author_id', 'content']
    for field in required_fields:
        if field not in data or not data[field]:
            return Response({"error": f"'{field}' is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Construct article data
    article_data = {
        "title": data.get("title"),
        "author_id": data.get("author_id"),
        "published_date": firestore.SERVER_TIMESTAMP,
        "summary": data.get("summary", ''),
        "tags": data.get("tags", []),
        "category": data.get("category", ''),
        "image_url": data.get("image_url", ''),
        "video_url": data.get("video_url", ''),
        "content": data.get("content", []),
        "attachments": data.get("attachments", []),
        "comments": [],
        "views": 0,
        "likes": 0,
        "shares": 0
    }

    try:
        # Add article to Firestore
        db.collection("articles").add(article_data)
        return Response({"message": "Article created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_article_by_id(request, article_id):
    try:
        doc_ref = db.collection('articles').document(article_id)
        doc_snapshot = doc_ref.get()

        if doc_snapshot.exists:
            article_data = doc_snapshot.to_dict()
            return Response(article_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_articles(request):
    try:
        articles_ref = db.collection('articles')
        articles_snapshot = articles_ref.get()

        articles = [doc.to_dict() for doc in articles_snapshot]
        return Response(articles, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_article(request, article_id):
    try:
        data = request.data
        doc_ref = db.collection('articles').document(article_id)

        doc_ref.update(data)
        return Response({"message": "Article updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_article(request, article_id):
    try:
        doc_ref = db.collection('articles').document(article_id)

        doc_ref.delete()
        return Response({"message": "Article deleted successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)