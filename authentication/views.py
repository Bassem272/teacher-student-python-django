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
import uuid
# Connection to the firestore
db = get_firestore_client()

# Function to get the next message ID
def get_next_user_id():
    return f'--user_{uuid.uuid4()}'
# @csrf_exempt ----.> we used create_user instead of this
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




@api_view(["POST"])
def create_user(request):
    data = json.loads(request.body)
    print("data", data)
    # Extract relevant fields from the JSON data
    email = data.get("email")
    # Check if email is already registered
    email_exists = db.collection("users").where("email", "==", email).get()
    
    if email_exists:
        print('email exists ')
        return JsonResponse({"message": "Email already exists"}, status=400)
    password = data.get("password")
    name = data.get("name")
    hashed_password = make_password(password)
    role = data.get("role")
    allowed_roles = ["teacher", "student", "parent"]  # Define allowed roles
    # Check if role is provided and valid
    if "role" in data and data["role"] == "admin":
        return JsonResponse({"message": "User cannot be assigned the role of admin"})
    if "role" not in data or data["role"] not in allowed_roles:
        return JsonResponse({"message": "Invalid user role"})
    courses = data.get("courses")
    children = data.get("children")
    # Generate a verification code
    verification_code = "".join(random.choices("0123456789", k=6))
    # Send verification code via email (you need to implement this part)
    send_verification_code_email(name, email, verification_code)
    # Store verification code in the session (you need to implement this part)
    request.session["verification_code"] = verification_code
    # Store additional user data in Firestore
    datao = {
        "user_id": get_next_user_id(),
         "credits" : 0,
        "email": email,
        "name": name,
        "avatar_url": "photo_url",
        "password": password,
        "email_verified": False,
        "verification_code": verification_code,
        "age": 18,
        "country": "country",
        "mobile": "mobile",
        "lastLogin": "lastLogin",
        "grade": "grade",
        "contacts":[],

        "token": "jwtToken",
        "role": role,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "courses": [],
        "children": [],

         "inbox": [],
    "sent_messages": [],
    "unread_messages": 2,
    "message_notifications_enabled": True,
    "blocked_users": [],
    "favorite_users": [],
    "notifications": [],
    "notification_settings": {
        "email": True,
        "push": True,
        "sms": False
    },
    "email_notifications_enabled": True,
    "push_notifications_enabled": True # Enable push notifications by default
        # Add more fields as needed
    }
    try:
        user_ref = db.collection("users").document()
        user_ref.set(datao)
        user_id = user_ref.id
    # return render(
    #     request,
    #     "ver_email.html",
    #     context={"user-data": user_ref, "userId": user_id, "verification_sent": True},
    # )
        return JsonResponse({"message": "User created successfully", "user_id": user_id})
    except Exception as e:
        print(f"the error is {e}")
        return JsonResponse({"error failed to create user:": str(e)}, status=500)
   


@api_view(["POST"])
def verify_email(request):
    data = json.loads(request.body)
    email = data.get("email")
    code = data.get("code")
    print(email, code)
    
    if not email or not code:
        return HttpResponseBadRequest("Missing email or code")

    try:
        # Get user documents matching the provided email
        user_ref = db.collection("users").where("email", "==", email).get()
        
        if not user_ref:
            return HttpResponseBadRequest("Invalid code or user does not exist")

        # Firestore query returns a list of documents, we need to iterate through them
        for doc in user_ref:
            user_data = doc.to_dict()
            stored_code = user_data.get("verification_code")

            if stored_code and code == stored_code:
                # Update the user's email_verified field
                db.collection("users").document(doc.id).update({"email_verified": True})
                
                # Set expiration time (e.g., 1 hour from now)
                expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
                
                # Generate JWT token with expiration time
                payload = {"email": email, "exp": expiration_time}
                token = jwt.encode(payload, "your_secret_key", algorithm="HS256")
                
                # Update the user's token
                db.collection("users").document(doc.id).update({"token": token})
                
                return JsonResponse({"message": "Email verified successfully", "token": token}, status=200)
        
        return HttpResponseBadRequest("Invalid code")
    
    except Exception as e:
        return HttpResponseBadRequest(f"An error occurred: {str(e)}")
    
    
@api_view(["POST"])
def login(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    try:
        # Retrieve user data from Firestore
        user_ref = db.collection("users").where("email", "==", email).get()
        
        id = user_ref[0].id
        if user_ref:
            user_data = user_ref[0].to_dict()
            hashed_password = user_data["password"]
            # Compare passwords
            # if check_password(password, hashed_password):
                # Authentication successful
                # Generate JWT token or perform any other necessary actions
                # Set expiration time (e.g., 1 hour from now)
            expiration_time = datetime.datetime.utcnow() + datetime.timedelta(
                    hours=100
                )
                # Generate JWT token with expiration time
            payload = {"email": email, "exp": expiration_time}
            token = jwt.encode(payload, "your_secret_key", algorithm="HS256")
            db.collection("users").document(id).update({"token": token})
                # Send token along with success message
            return Response(
                {"message": "Authentication successful", "token": token, "user_data":user_data}
                )
        #  else:
            # return Response({"error": "Invalid credentials"}, status=401)
        else:
            return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
def logout(request):
    data = json.loads(request.body)
    email = data.get("email")
    try:
        # Retrieve user data from Firestore
        user_ref = db.collection("users").where("email", "==", email).get()
        if user_ref:
            user_data = user_ref[0].to_dict()
            # Set token to null
            user_ref.update({"token": None})
            return Response({"message": "Logout successful"})
        else:
            return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
def ok(request):
    print("ok is here!")
    return Response({"message": "ok is ok !"})


@api_view(["PATCH"])
def update_password(request, id):
    data = json.loads(request.body)
    new_password = data.get("new_password")
    if not new_password:
        return HttpResponseBadRequest("Missing new password")

    try:
        user = db.collection("users").document(id)
        if user.get().exists:
            hashed_password = make_password(new_password)
            user.update({"password": hashed_password})
            return JsonResponse(
                {"message": "Password updated successfully"}, status=200
            )
        else:
            return HttpResponseNotFound("User not found")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# _______>_>______we first use reset_password_email then we use reset_password_form
@api_view(["POST"])
def reset_password_email(request):
    user_data = request.user_data
    if not user_data:
        return Response({"error": "User data not found"}, status=400)
    email = user_data.get("email")
    name = user_data.get("name")
    if not email:
        return Response({"error": "Email not found in user data"}, status=400)
    link = request.build_absolute_uri(reverse("reset_password_page"))
    # Send link via email (you need to implement this part)
    send_verification_code_email(name, email, link)
    return JsonResponse(
        {"message": "Email sent with the link for the reset password"}, status=200
    )


def reset_password_page(request):
    return render(request, "reset_password.html")


def reset_password_form(request):
    data = json.loads(request.body)
    new_password = data.get("new_password")
    email = data.get("email")

    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)
    if not new_password:
        return JsonResponse({"error": "New password is required"}, status=400)

    try:
        # Retrieve the user document reference based on the email
        user_ref = db.collection("users").where("email", "==", email).stream()

        # Check if any document matches the query
        found_user = False
        for doc in user_ref:
            found_user = True
            user_data = doc.to_dict()

            # Update the password field with the new hashed password
            hashed_password = make_password(new_password)
            doc.reference.update({"display_name": "go now"})
            doc.reference.update({"photo_url": "rul as is if "})
            doc.reference.update({"password": hashed_password})
            print(f"____{doc.id}________<><><><><><><><><>><>")
            reff = db.collection("users").document(doc.id).get()
            re = reff.to_dict()
            print(re)
            database_pass = re.get("password")
            if not check_password(new_password, database_pass):
                return JsonResponse({"error": "password is not the same "}, status=400)
            print("_________,.,.,.,.,___________")
            print(check_password)
            # Break the loop after updating the first matching document
            break

        if not found_user:
            return HttpResponseNotFound("User not found")

        return JsonResponse({"message": "Password updated successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def home(request):
    return render(request, "home.html")


@api_view(["DELETE"])
def delete_user(request, id):  # Change parameter name to 'id'
    try:
        # Delete user from Firebase Authentication

        # Delete user data from Firestore
        user_ref = db.collection("users").document(id)
        if user_ref.get().exists:
            user_ref.delete()
        else:
            return HttpResponseNotFound("User not found")
        return JsonResponse(
            {"message": "User and associated data deleted successfully"}, status=200
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
def get_user2(request, value):
    # Retrieve user information from Firebase Authentication using the UID
    print(request)
    user_ref = db.collection("users").document(value).get()  # this gets reference
    user_data = user_ref.to_dict()  # this gets snapshot
    emai = user_data["email"]
    print(emai)
    # print(user_ref2)
    print(user_ref.id)

    print(">>>>>>>)))))___________")
    # user_data = request.user_data
    return Response({"user": user_data})  # Example response


@api_view(["GET"])
def get_all_users(request):
    # Retrieve user information from Firebase Authentication using the UID
    print(request)
    all_users = []
    # map with the id as the key
    users_map = {}
    users_ref = db.collection("users").stream()  # this gets reference
    for doc in users_ref:
        users_map[doc.id] = doc.to_dict()
        user_data = doc.to_dict()  # this gets snapshot
        all_users.append(user_data)
    print(all_users)
    # print(user_ref2)
    print(">>>>>>>)))))___________")
    # user_data = request.user_data
    return Response({"users": all_users, "users_map": users_map})  # Example response

@api_view(["GET"])
def get_all_students(request):
    # Retrieve user information from Firebase Authentication using the UID
    print(request)
    all_students = []
    # map with the id as the key
    students_map = {}
    students_ref = db.collection("users").where("role", "==","student").stream()  # this gets reference
    for doc in students_ref:
        students_map[doc.id] = doc.to_dict()
        students_data = doc.to_dict()  # this gets snapshot
        all_students.append(students_data)
    print(all_students)
    # print(user_ref2)
    print(">>>>>>>)))))___________")
    # user_data = request.user_data
    return Response({"students": all_students, "students_map": students_map})  # Example response


@api_view(["GET"])
def get_all_teachers(request):
    # Retrieve user information from Firebase Authentication using the UID
    print(request)
    all_teachers = []
    # map with the id as the key
    teachers_map = {}
    teachers_ref = db.collection("users").where("role", "==","teacher").stream()  # this gets reference
    for doc in teachers_ref:
        teachers_map[doc.id] = doc.to_dict()
        teachers_data = doc.to_dict()  # this gets snapshot
        all_teachers.append(teachers_data)
    print(all_teachers)
    # print(user_ref2)
    print(">>>>>>>)))))___________")
    # user_data = request.user_data
    return Response({"teachers": all_teachers, "teachers_map": teachers_map})  # Example response

@api_view(["GET"])
def get_all_parents(request):
    # Retrieve user information from Firebase Authentication using the UID
    print(request)
    all_parents = []
    # map with the id as the key
    parents_map = {}
    parents_ref = db.collection("users").where("role", "==","parent").stream()  # this gets reference
    for doc in parents_ref:
        parents_map[doc.id] = doc.to_dict()
        parents_data = doc.to_dict()  # this gets snapshot
        all_parents.append(parents_data)
    print(all_parents)
    # print(user_ref2)
    print(">>>>>>>)))))___________")
    # user_data = request.user_data
    return Response({"parents": all_parents, "parents_map": parents_map})  # Example response




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
    # auth.send_email_verification(uid=uid)
    return JsonResponse({"message": "Verification email sent"})


def generate_access_token(user_id):
    # Generate JWT access token for the user (implementation not shown)
    # You might use a library like PyJWT to generate JWT tokens
    # Typically, this involves signing a token with a secret key and including user ID as a payload
    # Return the generated access token
    return "generated_access_token"
