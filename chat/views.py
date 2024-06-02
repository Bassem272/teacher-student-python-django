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
# @api_view(["POST"])
# def create_message(request):
#     data = json.loads(request.body)
#     if( not data ):
#         return JsonResponse({'message':'no body error bad request'},status=400)
    
#     content = data.get('content')
#     if(not content):
#         return JsonResponse({"message":'bad request no content for the message'}, status=400)
#     userEmail = data.get('email')
#     if(not userEmail):
#         return JsonResponse({"message":"no email sent form the user"}, status=400)
#     grade = data.get('grade')

#     try:
#         v= EmailValidator(userEmail)
#         userEmail = v['userEmail']

#         message = {
#             'userEmail':userEmail,
#             'content' : content,
#             'timeStamp':datetime.datetime.now(datetime.timezone.utc)
#         }
#         chat_grade_doc = db.collection('chat').document(grade)
#         if chat_grade_doc.exist():
#             chat_grade_doc.set(message, merge=True)
#             return JsonResponse({"message": "message added to the chat success"},status=201)
#         else:
#             return HttpResponseBadRequest("could not find the chat document")
#     except Exception as e:
#         return JsonResponse({"error was found":str(e)}, status=400)

# that was reviewed by perplexity
# @api_view(["POST"])
# def create_message(request):

#     try:
#         data = json.loads(request.body)
#         if not data:
#             return JsonResponse({'message': 'No body provided'}, status=400)

#         content = data.get('content')
#         if not content:
#             return JsonResponse({'message': 'No content provided'}, status=400)

#         email = data.get('email')
#         if not email:
#             return JsonResponse({'message': 'No email provided'}, status=400)

#         grade = data.get('grade')

#         if not grade:
#             return JsonResponse({'message': 'No grade provided'}, status=400)

#         email_validator = EmailValidator()
#         try:
#             v = email_validator(email)
#             email = v['email']
#         except ValidationError:
#             return JsonResponse({'message': 'Invalid email'}, status=400)

#         message = {
#             'userEmail': email,
#             'content': content,
#             'time': datetime.now(datetime.timezone.utc)
#         }

#         chat_grade_doc = db.collection('chat').document(grade)
#         if chat_grade_doc.exists():
#             chat_grade_doc.set(message, merge=True)
#             return JsonResponse({'message': 'Message added to the chat'}, status=201)
#         else:
#             return JsonResponse({'message': 'Could not find the chat document'}, status=404)

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
    
#     # revised by chatgpt 4.o and it estimated my experience to be 1-3 years 


# db = firestore.Client()

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
    chat_grade_doc_ref = db.collection('chat').document(grade).get()
    chat_grade_doc = chat_grade_doc_ref.to_dict()
    message_id = f'message_{len(chat_grade_doc) + 1}'
    print(message_id)
    message = {message_id: {
        'userEmail': userEmail,
        'content': content,
        'timeStamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    }
    try:

        chat_grade_doc_ref = db.collection('chat').document(grade)
        
        chat_grade_doc = chat_grade_doc_ref.get()
        if chat_grade_doc.exists:
            chat_grade_doc_ref.set(message, merge=True)

            chat_grade_doc_ref = db.collection('chat').document(grade).get()
            chat_grade_doc = chat_grade_doc_ref.to_dict()
            lista = list(chat_grade_doc.items())
            print(lista)
            last_message_id = list(chat_grade_doc.keys())[-1]
            chat_grade_doc_ref.set(message, merge=True)
            return JsonResponse({"message": "Message added to the chat successfully",
                                    "last_message_id": last_message_id,
                                    "chat_grade_doc": chat_grade_doc,
                                    }, status=201)
        else:
            return JsonResponse({"message": "Could not find the chat document"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@api_view(['delete'])
def delete_message(request, id):
    try: 
        data = json.loads(request.body)
        if(not data):
            return HttpResponseBadRequest('the body is empty') 
        if( not id): 
            return HttpResponseBadRequest("message id is not provided")
        grade = data.get('grade')
        if not grade:
            return JsonResponse({"message": "Grade is required"}, status=400)
        try:
            chat_doc_ref = db.collection('chat').document(grade).get()
            chat_doc_dict = chat_doc_ref.to_dict()
            chat_doc_list = list(chat_doc_dict.key())
            if(id not in chat_doc_list):
                return JsonResponse({"message": "Message not found"}, status=404)
            else:
                chat_doc_ref.update({id: firestore.DELETE})
                return JsonResponse({"message": "Message deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@api_view(['put'])    
def update_message(request,id):
    try:
        data = json.loads(request.body)
        if(not data):
            return HttpResponseBadRequest('the body is empty') 
        if( not id): 
            return HttpResponseBadRequest("message id is not provided")
        grade = data.get('grade')
        if not grade:
            return JsonResponse({"message": "Grade is required"}, status=400)
        content = data.get('content')
        if not content:
            return JsonResponse({"message": "Content is required"}, status=400)
        userEmail = data.get('userEmail')
        if not userEmail:
            return JsonResponse({"message": "User email is required"}, status=400)
        try:
            chat_doc_ref = db.collection('chat').document(grade).get()
            chat_doc_dict = chat_doc_ref.to_dict()
            chat_doc_list = list(chat_doc_dict.key())
            if(id not in chat_doc_list):
                return JsonResponse({"message": "Message not found"}, status=404)
            else:
                chat_doc_ref.set({{id:{
                    'content':content,
                    'userEmail':userEmail,
                    'timestamp':datetime.datetime.now(datetime.timezone.utc)

                }}})
                return JsonResponse({"message": "Message updated successfully",
                                     "message": chat_doc_dict[id]
                                     }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['get'])
def get_all_messages(request):
    try:
        data = json.loads(request.body)
        if(not data):
            return HttpResponseBadRequest('the body is empty') 
        grade = data.get('grade')
        if not grade:
            return JsonResponse({"message": "Grade is required"}, status=400)
        try:
            chat_doc_ref = db.collection('chat').document(grade).get()
            chat_doc_dict = chat_doc_ref.to_dict()
            chat_doc_list = list(chat_doc_dict.items())
            return JsonResponse({"message": "Messages fetched successfully",
                
                                     "messages": chat_doc_list
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)