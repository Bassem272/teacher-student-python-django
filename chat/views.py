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
from rest_framework.decorators import api_view, parser_classes
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
import random
from django.http import JsonResponse, HttpResponseBadRequest,HttpResponseNotFound
# from .email_code import send_verification_code_email
from firebase_admin import firestore
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
import threading
import uuid
from rest_framework.parsers import MultiPartParser, FormParser
import os
from firestore_utils import get_firestore_client

# Connection to the firestore
db, storage_bucket = get_firestore_client()

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
        try:
            files = request.FILES.getlist('file')
            uploaded_file_urls = []

            bucket_name= 'gs://dragna272.appspot.com'
 # Replace with your bucket name

            for file in files:
                # blob_name = os.path.join('uploads', file.name)  # Example path in the bucket
                blob_name = f'uploads/{file.name}'
                # Initialize bucket and blob
                blob = storage_bucket.blob(blob_name)

                # Upload the file to Firebase Storage
                blob.upload_from_file(file, content_type=file.content_type)

                # Optionally, make the blob publicly accessible
                blob.make_public()

                # Get the public URL of the uploaded file
                file_url = blob.public_url
                uploaded_file_urls.append(file_url)

            return JsonResponse({'uploaded_file_urls': uploaded_file_urls}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
        

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request,'chat/room.html',{'room_name':room_name})

# Define a global counter for message IDs
message_id_counter = 0

# Create a lock to synchronize access to the counter
lock = threading.Lock()

# Function to get the next message ID
def get_next_message_id():
    # global message_id_counter
    # with lock:
    #     message_id_counter += 1
    #     return f'++message_{message_id_counter}'
    return f'--message_{uuid.uuid4()}'

time = datetime.datetime.now(datetime.timezone.utc).isoformat()
@api_view(["POST"])
def create_message(request):
   
    # try:
    data = json.loads(request.body)
    print("@@@ create_message @@@", request.body)

    # except json.JSONDecodeError:
    #     return JsonResponse({'message': 'Invalid JSON'}, status=400)

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
    type =  data.get('type')
    if type == 'file':
        fileUrl = data.get('fileUrl')
        print('type:::::::::::::::::::::::::file')
        if not fileUrl:
            return JsonResponse({'message':'fileUrl is required '} , status=400)
    else:
        print('type:::::::::::::::::::::::::not______file')
        fileUrl=''    
    name = data.get('name') 
    if not name:
        return JsonResponse({'message':'name is required '}, status=400)
    avatar_url = data.get('avatar_url')
    if not avatar_url:
        return JsonResponse({"message":'avatar_url is required '}, status=400)
    print('filetttttttttttttttttttttttttttttttttttt',fileUrl)
    chat_grade_doc_ref = db.collection('chat').document(grade).get()
    chat_grade_doc = chat_grade_doc_ref.to_dict()
    message_id = get_next_message_id()
    # print(message_id)
    message = {
        "type": type,
        "message_id": message_id,
        'content': content,
        "name": name,
        'email': userEmail,
        'time': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "avatar_url": avatar_url,
        "fileUrl":fileUrl
    }
    
    try:
        chat_grade_doc_ref = db.collection('chat').document(message_id)
        chat_grade_doc_ref.set(message)
    
        chat_grade_doc_ref = db.collection('chat')
        chat_docs = chat_grade_doc_ref.stream()
        chat_map = { doc.id: doc.to_dict() for doc in chat_docs}
    
        if chat_map:
        
            lista = list(chat_map.items())
            # print('lista---------------',lista)
            lista_sorted = sorted(lista, key=lambda x: x[1]['time'])
     
            return JsonResponse({"message": "Message added to the chat successfully",
                            
                                    "messages_sorted":lista_sorted
                                    }, status=201)
        else:
            return JsonResponse({"message": "Could not find the chat document"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

# @api_view(['delete'])
# def delete_message(request, id):
#     try: 
#         data = json.loads(request.body)
#         if(not data):
#             return HttpResponseBadRequest('the body is empty') 
#         if( not id): 
#             return HttpResponseBadRequest("message id is not provided")
#         grade = data.get('grade')
#         if not grade:
#             return JsonResponse({"message": "Grade is required"}, status=400)
#         try:
#             chat_doc_ref_snapShot = db.collection('chat').document(grade)
#             chat_doc_ref = db.collection('chat').document(grade).get()
#             chat_doc_dict = chat_doc_ref.to_dict()
#             chat_doc_list = list(chat_doc_dict.keys())
#             if(id not in chat_doc_list):
#                 return JsonResponse({"message": "Message not found"}, status=404)
#             else:
#                 chat_doc_ref_snapShot.update({id: firestore.DELETE})
#                 return JsonResponse({"message": "Message deleted successfully"}, status=200)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
    

@api_view(['DELETE'])
def delete_message(request, id):
    try:
        data = json.loads(request.body)
        if not data:
            return HttpResponseBadRequest('The body is empty')
        if not id:
            return HttpResponseBadRequest("Message id is not provided")
        
        grade = data.get('grade')
        if not grade:
            return JsonResponse({"message": "Grade is required"}, status=400)
        
        try:
            chat_doc_ref = db.collection('chat').document(grade)
            chat_doc_snapshot = chat_doc_ref.get()
            chat_doc_dict = chat_doc_snapshot.to_dict()
            
            if not chat_doc_dict or id not in chat_doc_dict:
                return JsonResponse({"message": "Message not found"}, status=404)
            else:
                chat_doc_ref.update({id: firestore.DELETE_FIELD})
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
        userEmail = data.get('email')
        if not userEmail:
            return JsonResponse({"message": "User email is required"}, status=400)
        try:
            chat_doc_ref = db.collection('chat').document(grade)
            chat_doc_dict = chat_doc_ref.get().to_dict()
            chat_doc_list = list(chat_doc_dict.keys())
            if(id not in chat_doc_list):
                return JsonResponse({"message": "Message not found"}, status=404)
            else:
                chat_doc_ref.set({id:{
                    'content':content,
                    'userEmail':userEmail,
                    'timestamp':datetime.datetime.now(datetime.timezone.utc)

                }})
                return JsonResponse({"message": "Message updated successfully",
                                     "edited-old" : chat_doc_dict.get(id)
                                    
                                            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['get'])
def get_all_messages(request  , grade):
        try:
            chat_doc_ref = db.collection('chat').stream()
            chat_map = {doc.id : doc.to_dict() for doc in chat_doc_ref}
            if chat_map: 
                chat_list = list(chat_map.items())
                chat_list_sorted = sorted(chat_list , key= lambda x:x[1]['time'])
                # print('all_messages************',chat_list_sorted)
            # chat_doc_dict = chat_doc_ref.to_dict()
            # chat_doc_list = list(chat_doc_dict.items())
             # Sort messages by time (second element in each tuple)
            # chat_doc_list_sorted = sorted(chat_doc_list, key=lambda x: x[1]['time'])
            # print(f'we have a chat messages success ------{time}', chat_list_sorted[-1])
            return JsonResponse({"message": "Messages fetched successfully",
                
                                    "messages": chat_list_sorted
            })
        except Exception as e:
            print(f'error is {e}')
            return JsonResponse({"error is-": str(e)}, status=500)
        
    # except Exception as e:
    #     print(f'overall error is {e}')
    #     return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['delete'])
def delete_all_messages(request):
    try:
        data = json.loads(request.body)
        if(not data):
            return HttpResponseBadRequest('the body is empty')
        grade = data.get('grade')
        if not grade:
            return JsonResponse({"message": "Grade is required"}, status=400)
        try:
            chat_doc_ref = db.collection('chat').document(grade)
            chat_doc_ref.set({},merge=False)
            return JsonResponse({"message": "Messages deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
