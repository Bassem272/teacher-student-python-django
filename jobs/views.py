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
#   "id": "job1",
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
def create_job(request):
    data = json.loads(request.body)
    title = data.get("title")
    author = data.get("author")
    date = data.get("date")
    content = data.get("content")
    tags = data.get("tags")

    if not title or not author or not date or not content or not tags:
        return HttpResponseBadRequest("Missing required fields")

    # Generate a unique job ID with a prefix
    job_id = f"job_{uuid.uuid4()}"
    job_data = {
        "id": job_id,
        "author": author,
        "title": title,
        "date": date,
        "content": content,
        "tags": tags,
    }
    try:
        db.collection('jobs').document(job_id).set(job_data)
        return JsonResponse(
            {"message": "Job created successfully", "job_data": job_data},
            status=201,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    # data = json.loads(request.body)
    # print(data)
    # return Response({"message": "Hello, World! from jobs!"})

from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt

# @api_view(["POST"])
# def create_job(request):
#     data = json.loads(request.body)
#     print(data)
#     title = data.get("title")
#     author = data.get("author")
#     date = data.get("date")
#     content = data.get("content")
    
#     tags = data.get("tags")
#     if not author or not title  or not content or date or not tags:
#         return HttpResponseBadRequest("Missing required fields")

#     # Generate a unique job ID with a prefix
#     job_id = f"job_{uuid.uuid4()}"
#     job_data = {
#         "id": job_id,
#         "author": author,
#         "title": title,
#         "date": date,
#         "content": content,
#         "tags": tags,
        
#     }
#     try:
#         db.collection('jobs').document(job_id).set(job_data)
#         return JsonResponse(
#             {"message": "job created successfully", "job_data": job_data},
#             status=201,
#         )
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
def get_job(request,  job_id):
    logger.info(f"get_job is here: { job_id}")
    try:
        doc_ref = db.collection('jobs').document(job_id)
        doc = doc_ref.get()
        if doc.exists:
            job_data = doc.to_dict()
            logger.info(f"job found: {job_data}")
            return JsonResponse({"job_data": job_data}, status=200)
        else:
            return JsonResponse({"error": "job not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(["GET"])    
def get_all_jobs(request):
    try:
        jobs = []
        docs = db.collection('jobs').get()
        for doc in docs:
            job_data = doc.to_dict()
            jobs.append(job_data)
            
        return JsonResponse({"jobs": jobs}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
