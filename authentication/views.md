from django.http import JsonResponse
from firebase_admin import firestore
from .firebase_config import get_firestore_client

def create_user(request):
    # Parse request data
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    # Validate data (not shown)

    # Create user document in Firestore
    db = get_firestore_client()
    user_ref = db.collection('users').add({
        'username': username,
        'email': email,
        'password': password
    })
    user_id = user_ref.id

    return JsonResponse({'user_id': user_id})

def get_user(request, user_id):
    # Retrieve user document from Firestore
    db = get_firestore_client()
    user_doc = db.collection('users').document(user_id).get().to_dict()

    if user_doc:
        return JsonResponse(user_doc)
    else:
        return JsonResponse({'error': 'User not found'}, status=404)

def update_user(request, user_id):
    # Parse request data
    new_username = request.POST.get('username')
    new_email = request.POST.get('email')

    # Update user document in Firestore
    db = get_firestore_client()
    db.collection('users').document(user_id).update({
        'username': new_username,
        'email': new_email
    })

    return JsonResponse({'message': 'User updated successfully'})

def delete_user(request, user_id):
    # Delete user document from Firestore
    db = get_firestore_client()
    db.collection('users').document(user_id).delete()

    return JsonResponse({'message': 'User deleted successfully'})
