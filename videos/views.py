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
#   "id": "video1",
#   "grade": 1,
#   "title": "Math Lesson",
#   "description": "Basic math concepts",
#   "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
#   "tags": ["math", "grade 1"]
# }

@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello, World! from videos!"})

@api_view(["POST"])
def create_video(request, grade_id):
    data = json.loads(request.body)
    grade = data.get("grade")
    title = data.get("title")
    description = data.get("description")
    video_url = data.get("video_url")
    tags = data.get("tags")
    if not grade or not title or not description or not video_url or not tags:
        return HttpResponseBadRequest("Missing required fields")

    # Generate a unique video ID with a prefix
    video_id = f"video_{uuid.uuid4()}"
    video_data = {
        "id": video_id,
        "grade": grade,
        "title": title,
        "description": description,
        "video_url": video_url,
        "tags": tags,
    }
    try:
        db.collection(grade_id).document(video_id).set(video_data)
        return JsonResponse(
            {"message": "Video created successfully", "video_data": video_data},
            status=201,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
def get_video(request, grade_id, video_id):
    logger.info(f"get_video is here: {grade_id , video_id}")
    try:
        doc_ref = db.collection(grade_id).document(video_id)
        doc = doc_ref.get()
        if doc.exists:
            video_data = doc.to_dict()
            logger.info(f"Video found: {video_data}")
            return JsonResponse({"video_data": video_data}, status=200)
        else:
            return JsonResponse({"error": "Video not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(["GET"])    
def get_all_videos(request, grade_id):
    try:
        videos = []
        docs = db.collection(grade_id).get()
        for doc in docs:
            video_data = doc.to_dict()
            videos.append(video_data)
            
        return JsonResponse({"videos": videos}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
