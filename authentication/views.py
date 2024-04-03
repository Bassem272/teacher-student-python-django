from telnetlib import STATUS
from django.shortcuts import render
from django.urls import reverse
from grpc import Status
from requests import Response
from cplatform.firestore_utils import get_firestore_client
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from firebase_admin import auth, credentials
from rest_framework import status
from rest_framework.response import Response
from firebase_admin import auth
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


# Connection to the firestore
db = get_firestore_client()


# @csrf_exempt
def register(request):
    if request.method == "POST":
        # Get the user input from the request
        # username = request.POST.get("username")
        # email = request.POST.get("email")
        # password = request.POST.get("password")
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Check if all required fields are provided
        if not username or not email or not password:
            return JsonResponse(
                {"error": "Username, email, and password are required."}, status=400
            )

        # Check if the username already exists
        user_ref = db.collection("users").document(username)
        if user_ref.get().exists:
            return JsonResponse({"error": "Username already exists."}, status=400)

        # Create a new user document
        user_data = {"username": username, "email": email, "password": password}
        user_ref.set(user_data)

        # Check if the user document was successfully created
        if user_ref.get().exists:
            return JsonResponse(
                {"success": "User registered successfully."}, status=201
            )
        else:
            return JsonResponse({"error": "Failed to register user."}, status=500)

    else:
        return JsonResponse(
            {"error": "Only POST requests are allowed for this endpoint."}, status=405
        )


# def create_user(request):
#     # Extract email and password from the request body
#     data = json.loads(request.body)
#     email = data.get("email")
#     password = data.get("password")

#     # Check if email and password are provided
#     if not email or not password:
#         return JsonResponse(
#             {"error": "Email and password are required"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     # try:
#     # Create a new user in Firebase Authentication with the provided email and password
#     user = auth.create_user(email=email, password=password)
#     return JsonResponse({"userid": user.uid}, status=201)
from django.shortcuts import render
from django.core.mail import send_mail
from .email import send_ver_email
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseBadRequest



# this is the best for creating  the user 00000000000
# @api_view(["POST"])
# def create_user(request):
#     data = json.loads(request.body)

#     # Extract relevant fields from the JSON data
#     email = data.get("email")
#     password = data.get("password")
#     name = data.get("name")

#     # Create user in Firebase Authentication
#     user_record = auth.create_user(email=email, password=password, display_name=name)
    
#     # Send email verification request
#     auth.generate_email_verification_link(email)
#     # Generate verification token
#     # verification_token = default_token_generator.make_token(user_record.uid)

#     # verification_link = request.build_absolute_uri(
#     #     reverse("verify_email") + f"?email={email}&token={verification_token}"
#     # )

#     send_ver_email(email, name, verification_link=verification_link)
#     # Store additional user data in Firestore
#     user_data = {
#         "email": email,
#         "display_name": name,
#         "photo_url": "photo_url",
#         "password": password,
#         "email_verified": False,
#         # Add more fields as needed
#     }
#     user_ref = db.collection("users").document(user_record.uid)
#     user_ref.set(user_data)

#     return JsonResponse(
#         {"user-data": user_data, "userid": user_record.uid, "verification_sent": True},
#         status=201,
#     )


# def verify_email(request):
#     email = request.GET.get('email')
#     token = request.GET.get('token')
    
#     if not email or not token:
#         return HttpResponseBadRequest("Missing email or token")

#     try:
#         # Verify email in Firebase Authentication
#         decoded_token = auth.verify_email_verification_token(token)
#         if decoded_token['email'] == email:
#             # Mark email as verified in Firestore
#             user = auth.get_user(email)
#             # user = get_user_model().objects.get(email=email)
#             user_ref = db.collection("users").document(user.uid)
#             user_ref.update({"email_verified": True})
#             return JsonResponse({"message": "Email verified successfully"}, status=200)
#         else:
#             return HttpResponseBadRequest("Invalid token")
#     except auth.InvalidTokenError:
#         return HttpResponseBadRequest("Invalid token")

import random
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from firebase_admin import auth
from .email_code import send_verification_code_email

@api_view(["POST"])
def create_user(request):
    data = json.loads(request.body)

    # Extract relevant fields from the JSON data
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    # Generate a verification code
    verification_code = ''.join(random.choices('0123456789', k=6))

    # Create user in Django User model
    user = User.objects.create_user(username=email, email=email, password=password, first_name=name)

    # Send verification code via email (you need to implement this part)
    send_verification_code_email(name, email, verification_code)

    # Store verification code in the session (you need to implement this part)
    request.session['verification_code'] = verification_code

    # Store additional user data in Firestore
    datao = {
        "email": email,
        "display_name": name,
        "photo_url": "photo_url",
        "password": password,
        "email_verified": False,
        # Add more fields as needed
    }
    user_ref = db.collection("users").document(str(user.pk))
    user_ref.set(datao)

    return render(request,"ver_email.html",
      context={
            "user-data": datao, 
            "userid": user.pk, 
            "verification_sent": True
      }
    )


@api_view(["POST"])
def verify_email(request):
    data = json.loads(request.body)
    email = data.get('email')
    code = data.get('code')
    print(email, code)
    if not email or not code:
        return HttpResponseBadRequest("Missing email or code")

    try:
        # Get verification code from the session
        stored_code = request.session.get('verification_code')
        if stored_code and code == stored_code:
            # Clear verification code from session
            del request.session['verification_code']

            # Activate the user and update email_verified field in Firestore
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            user_ref = db.collection("users").document(str(user.pk))
            user_ref.update({"email_verified": True})

            return JsonResponse({"message": "Email verified successfully"}, status=200)
        else:
            return HttpResponseBadRequest("Invalid code")
    except User.DoesNotExist:
        return HttpResponseBadRequest("User does not exist")



# app/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')




@api_view(["DELETE"])
def delete_user(request, uid):  # Change parameter name to 'uid'
    try:
        # Delete user from Firebase Authentication
        auth.delete_user(uid)

        # Delete user data from Firestore
        db.collection("users").document(uid).delete()

        return JsonResponse(
            {"message": "User and associated data deleted successfully"}, status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

























# def create_user(request):
#     # Extract email and password from the request body
#     data = json.loads(request.body)
#     email = data.get('email')
#     password = data.get('password')

#     # Check if email and password are provided
#     if not email or not password:
#         return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Create a new user in Firebase Authentication with the provided email and password
#         user = auth.create_user(email=email, password=password)
#         return Response({'uid': user.uid}, status=status.HTTP_201_CREATED)
#     except FirebaseError as e:
#         # Handle Firebase Authentication errors
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# def get_user(request, uid):

#     # Retrieve user information from Firebase Authentication using the UID
#     user_record = get_user(
#         uid
#     )  # Assuming get_user is a function to retrieve the UserRecord object
#     user_data = {
#         "uid": user_record.uid,
#         "email": user_record.email,
#         # Add more user attributes as needed
#     }
#     return JsonResponse({"user_data": user_data}, status=200)

#     # Handle errors


def get_user1(request, id):
    return JsonResponse({"id": id})


@api_view(["GET"])
def get_user2(request, value):
    # Retrieve user information from Firebase Authentication using the UID
    user_record = auth.get_user(
        value
    )  # Assuming get_user is a function to retrieve the UserRecord object
    user_data = {
        "uid": user_record.uid,
        "email": user_record.email,
        # Add more user attributes as needed
    }
    return JsonResponse({"user_data": user_data}, status=200)


# return JsonResponse({'id': value})


def update_user_display_name(uid, display_name):
    # """
    # Updates the display name of a user in Firebase Authentication.

    # Args:
    #     uid (str): UID of the user.
    #     display_name (str): New display name for the user.

    # Returns:
    #     firebase_admin.auth.UserRecord: Updated user record object.
    # """
    user = auth.update_user(uid, display_name=display_name)
    return user


def send_verification_email(uid):
    # """
    # Sends a verification email to the user with the provided UID.

    # Args:
    #     uid (str): UID of the user.
    # """
    auth.send_email_verification(uid=uid)
    return JsonResponse({"message": "Verification email sent"})


def login(request):
    if request.method == "POST":
        # Extract user credentials from request data
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Authenticate user with Firebase
            user = auth.get_user_by_email(email)
            if user.password == password:
                pass
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

            # If user is found and password matches, generate access token
            # (Note: This is a simplified example. Actual authentication process may vary)
            # Here, you might also perform additional checks like verifying the email is verified, etc.
            access_token = generate_access_token(user.uid)

            # Return access token in response
            return JsonResponse({"access_token": access_token})
        except auth.AuthError as e:
            # Handle authentication errors
            return JsonResponse({"error": "Authentication failed"}, status=401)

    else:
        # Handle unsupported request methods
        return JsonResponse({"error": "Method not allowed"}, status=405)


def generate_access_token(user_id):
    # Generate JWT access token for the user (implementation not shown)
    # You might use a library like PyJWT to generate JWT tokens
    # Typically, this involves signing a token with a secret key and including user ID as a payload
    # Return the generated access token
    return "generated_access_token"
