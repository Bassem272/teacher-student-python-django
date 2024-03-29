from django.shortcuts import render
from cplatform.firestore_utils import get_firestore_client
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Connection to the firestore
db = get_firestore_client()


@csrf_exempt
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
