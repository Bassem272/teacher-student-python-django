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

# views/channel_views.py

@api_view(['POST'])
def create_channel(request):
    try:
        data = request.data
        channel_name = data.get('name')
        grade_level = data.get('grade_level')
        description = data.get('description', '')
        admin_id = data.get('admin_id')

        if not channel_name or not grade_level or not admin_id:
            return Response({"error": "Name, grade level, and admin ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        channel_data = {
            "name": channel_name,
            "description": description,
            "grade_level": grade_level,
            "created_at": firestore.SERVER_TIMESTAMP,
            "admin_id": admin_id,
            "subscribers": []
        }

        db.collection('channels').add(channel_data)
        return Response({"message": "Channel created successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_channel_by_id(request, channel_id):
    try:
        doc_ref = db.collection('channels').document(channel_id)
        doc_snapshot = doc_ref.get()

        if doc_snapshot.exists:
            channel_data = doc_snapshot.to_dict()
            return Response(channel_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_channels(request):
    try:
        channels_ref = db.collection('channels')
        channels_snapshot = channels_ref.get()

        channels = [doc.to_dict() for doc in channels_snapshot]
        return Response(channels, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def update_channel(request, channel_id):
    try:
        data = request.data
        doc_ref = db.collection('channels').document(channel_id)

        doc_ref.update(data)
        return Response({"message": "Channel updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_channel(request, channel_id):
    try:
        doc_ref = db.collection('channels').document(channel_id)

        doc_ref.delete()
        return Response({"message": "Channel deleted successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)