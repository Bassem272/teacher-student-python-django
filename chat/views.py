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


from firestore_utils import get_firestore_client

# Connection to the firestore
db = get_firestore_client()
# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request,'chat/room.html',{'room_name':room_name})
from django.core.validators import MaxLengthValidator, EmailValidator
from django.core.exceptions import ValidationError


# that was written by me 
@api_view(["POST"])
def create_message(request):
    data = json.loads(request.body)
    if( not data ):
        return JsonResponse({'message':'no body error bad request'},status=400)
    
    content = data.get('content')
    if(not content):
        return JsonResponse({"message":'bad request no content for the message'}, status=400)
    userEmail = data.get('email')
    if(not userEmail):
        return JsonResponse({"message":"no email sent form the user"}, status=400)
    grade = data.get('grade')

    try:
        v= EmailValidator(userEmail)
        userEmail = v['userEmail']

        message = {
            'userEmail':userEmail,
            'content' : content,
            'timeStamp':datetime.datetime.now(datetime.timezone.utc)
        }
        chat_grade_doc = db.collection('chat').document(grade)
        if chat_grade_doc.exist():
            chat_grade_doc.set(message, merge=True)
            return JsonResponse({"message": "message added to the chat success"},status=201)
        else:
            return HttpResponseBadRequest("could not find the chat document")
    except Exception as e:
        return JsonResponse({"error was found":str(e)}, status=400)

# that was reviewed by perplexity
@api_view(["POST"])
def create_message(request):

    try:
        data = json.loads(request.body)
        if not data:
            return JsonResponse({'message': 'No body provided'}, status=400)

        content = data.get('content')
        if not content:
            return JsonResponse({'message': 'No content provided'}, status=400)

        email = data.get('email')
        if not email:
            return JsonResponse({'message': 'No email provided'}, status=400)

        grade = data.get('grade')

        if not grade:
            return JsonResponse({'message': 'No grade provided'}, status=400)

        email_validator = EmailValidator()
        try:
            v = email_validator(email)
            email = v['email']
        except ValidationError:
            return JsonResponse({'message': 'Invalid email'}, status=400)

        message = {
            'userEmail': email,
            'content': content,
            'time': datetime.now(datetime.timezone.utc)
        }

        chat_grade_doc = db.collection('chat').document(grade)
        if chat_grade_doc.exists():
            chat_grade_doc.set(message, merge=True)
            return JsonResponse({'message': 'Message added to the chat'}, status=201)
        else:
            return JsonResponse({'message': 'Could not find the chat document'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    # revised by chatgpt 4.o and it estimated my experience to be 1-3 years 
    from django.http import JsonResponse, HttpResponseBadRequest
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from google.cloud import firestore
import json
import datetime
from rest_framework.decorators import api_view

db = firestore.Client()

@api_view(["POST"])
def create_message(request):
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

    email_validator = EmailValidator()
    try:
        email_validator(userEmail)
    except ValidationError:
        return JsonResponse({"message": "Invalid email format"}, status=400)

    grade = data.get('grade')
    if not grade:
        return JsonResponse({"message": "Grade is required"}, status=400)

    message = {
        'userEmail': userEmail,
        'content': content,
        'timeStamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    try:
        chat_grade_doc_ref = db.collection('chat').document(grade)
        chat_grade_doc = chat_grade_doc_ref.get()
        if chat_grade_doc.exists:
            chat_grade_doc_ref.set(message, merge=True)
            return JsonResponse({"message": "Message added to the chat successfully"}, status=201)
        else:
            return JsonResponse({"message": "Could not find the chat document"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
