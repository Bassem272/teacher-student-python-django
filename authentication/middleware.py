# authentication/middleware.py

import json
from django import db
from django.contrib.auth import get_user_model
from django.http import JsonResponse

# User = get_user_model()

import jwt
from django.http import JsonResponse
import datetime
from firebase_admin import firestore

class TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Extract JWT token from request headers
            authorization_header = request.headers.get('Authorization')
            if authorization_header:
                try:
                    # Extract token from the header (assuming it starts with 'Bearer ')
                    token = authorization_header.split(' ')[1]
                    # Decode and verify the JWT token
                    payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
                    # Check token expiration
                    if 'exp' in payload and payload['exp'] >= datetime.datetime.utcnow().timestamp():
                        # Attach user information to the request for downstream views/middleware
                        request.user_info = payload
                    else:
                        return JsonResponse({"error": "Token has expired"}, status=401)
                except jwt.ExpiredSignatureError:
                    return JsonResponse({"error": "Token has expired"}, status=401)
                except jwt.InvalidTokenError:
                    return JsonResponse({"error": "Invalid token"}, status=401)
            else:
                return JsonResponse({"error": "Authorization header missing"}, status=401)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response

class RoleBasedAccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user_info exists in the request (set by TokenValidationMiddleware)
        if hasattr(request, 'user_info'):
            # Extract user role from user_info
            user_role = request.user_info.get('role')

            # Implement your role-based access control logic here
            if user_role == 'admin':
                # Grant access to admin-only endpoints
                pass
            elif user_role == 'user':
                # Grant access to user-only endpoints
                pass
            else:
                return JsonResponse({"error": "Unauthorized"}, status=403)

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response
