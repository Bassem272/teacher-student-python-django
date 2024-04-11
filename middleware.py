# authentication/middleware.py

import json
from django import db
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from authentication import views
from firestore_utils import get_firestore_client
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import jwt
import datetime


# Connection to the firestore
db = get_firestore_client()
# User = get_user_model()

import jwt
from django.http import JsonResponse
import datetime
from firebase_admin import firestore

# this to ensure logging in

class TokenValidationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
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
                        # Call the next middleware or view with the 'value' argument
                        return self.get_response(request, *args, **kwargs)
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

class AnotherMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       # Check if user_info exists in the request (set by TokenValidationMiddleware)
        if hasattr(request, 'user_info'):
            # Extract user role from user_info
            user_role = request.user_info.get('role')

            # Implement your role-based access control logic here
            if user_role != 'teacher':
                return JsonResponse({"error": "Access denied. Only teachers are allowed to access this resource."}, status=403)


        # Pass the request to the next middleware or view
            JsonResponse({"message": "another one "}, status=403)
            response = self.get_response(request)
        return response
    

class VerifiedEmail:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return JsonResponse({"message": "Email is required"}, status=400)
        
        # Check if the email exists in the request
        user_ref = db.collection('users').where('email', '==', email).get()
        if not user_ref:
            return JsonResponse({"message": "User not found"}, status=404)
        print(user_ref)
        user_data = user_ref[0].to_dict()
        print(user_data)
        # Check if the user's email is verified
        if not user_data.get('email_verified'):
            return JsonResponse({"message": 'User email is not verified'}, status=400)
          # Attach user_data to the request
        request.user_data = user_data
        response = self.get_response(request)
        return response

from django.http import JsonResponse

class TeacherAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user_info exists in the request (set by TokenValidationMiddleware)
        if hasattr(request, 'user'):
            # Extract user role from user
            user_role = request.user.get('role')

            # Implement your role-based access control logic here
            if user_role != 'teacher':
                return JsonResponse({"error": "Access denied. Only teachers are allowed to access this resource."}, status=403)

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response

class StudentAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user exists in the request (set by TokenValidationMiddleware)
        if hasattr(request, 'user'):
            # Extract user role from user
            user_role = request.user.get('role')

            # Implement your role-based access control logic here
            if user_role != 'student':
                return JsonResponse({"error": "Access denied. Only students are allowed to access this resource."}, status=403)

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response

class ParentAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user exists in the request (set by TokenValidationMiddleware)
        if hasattr(request, 'user'):
            # Extract user role from user
            user_role = request.user.get('role')

            # Implement your role-based access control logic here
            if user_role != 'parent':
                return JsonResponse({"error": "Access denied. Only parents are allowed to access this resource."}, status=403)

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user exists in the request (set by TokenValidationMiddleware)
        if hasattr(request, 'user'):
            # Extract user role from user
            user_role = request.user.get('role')

            # Implement your role-based access control logic here
            if user_role != 'admin':
                return JsonResponse({"error": "Access denied. Only admins are allowed to access this resource."}, status=403)

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response


