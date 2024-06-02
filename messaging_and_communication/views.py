from django.http import JsonResponse
from django.shortcuts import render
from requests import Response
from telnetlib import STATUS
from django.shortcuts import render
from grpc import Status
from requests import Response

from firestore_utils import get_firestore_client
from rest_framework.decorators import api_view
# Connection to the firestore
db = get_firestore_client()
# Create your views here.

@api_view(["GET"])
def get_inbox(request, id):
    try:
        user_ref = db.collection("users").document(id)
        user_data = user_ref.get().to_dict()
        if user_data:
            inbox = user_data.get("inbox", [])
            return JsonResponse({"inbox": inbox}, status=200)
        else:
            return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# @api_view(["GET"])
# def get_notifications(request,id):
#     try:
#         user_ref = db.collection("users").document(id)
#         user_data = user_ref.get().to_dict()
#         if user_data:
#             notifications = user_data.get("notifications", [])
#             return  JsonResponse({"notifications": notifications})
#         else:
#             return JsonResponse({"error": "User not found"}, status=404)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

@api_view(["GET"])
def get_notifications(request,id):
    try:
        user_ref = db.collection("users").document(id)
        user_data = user_ref.get().to_dict()
        if user_data:
            notifications = user_data.get("notifications", [])
            return JsonResponse({"notifications": notifications})
        else:
            return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(["POST"])
def send_message(request, sender_id, receiver_id):
    try:
        message = request.data.get("message")
        if not message:
            return JsonResponse({"error": "Message body is required"}, status=400)
        
        sender_ref = db.collection("users").document(sender_id)
        receiver_ref = db.collection("users").document(receiver_id)
        
        sender_data = sender_ref.get().to_dict()
        receiver_data = receiver_ref.get().to_dict()
        
        if not sender_data or not receiver_data:
            return JsonResponse({"error": "Sender or receiver not found"}, status=404)
        
        # Add message to sender's sent messages
        sent_messages = sender_data.get("sent_messages", [])
        sent_messages.append({"receiver_id": receiver_id, "message": message})
        sender_ref.update({"sent_messages": sent_messages})
       

        
        # Add message to receiver's inbox
        inbox = receiver_data.get("inbox", [])
        inbox.append({"sender_id": sender_id, "message": message, "read": False})
        receiver_ref.update({"inbox": inbox})
         # add notifications for the receiver
        notifications = receiver_data.get("notifications", [])
        notifications.append({"sender_id": sender_id, "message": message})
        receiver_ref.update({"notifications": notifications})
        
        return JsonResponse({"message": "Message sent successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(["PUT"])
def mark_message_as_read(request, id, message_index):
    try:
        user_ref = db.collection("users").document(id)
        user_data = user_ref.get().to_dict()
        if not user_data:
            return JsonResponse({"error": "User not found"}, status=404)
        
        inbox = user_data.get("inbox", [])
        if 0 <= message_index < len(inbox):
            inbox[message_index]["read"] = True
            user_ref.update({"inbox": inbox})
            return JsonResponse({"message": "Message marked as read"})
        else:
            return JsonResponse({"error": "Message index out of range"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(["DELETE"])
def delete_message(request, id, message_index):
    try:
        user_ref = db.collection("users").document(id)
        user_data = user_ref.get().to_dict()
        if not user_data:
            return JsonResponse({"error": "User not found"}, status=404)
        
        inbox = user_data.get("inbox", [])
        if 0 <= message_index < len(inbox):
            del inbox[message_index]
            user_ref.update({"inbox": inbox})
            return JsonResponse({"message": "Message deleted successfully"})
        else:
            return JsonResponse({"error": "Message index out of range"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(["DELETE"])
def clear_inbox(request, id):
    try:
        user_ref = db.collection("users").document(id)
        user_ref.update({"inbox": []})
        return JsonResponse({"message": "Inbox cleared successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(["PUT"])
def mark_all_messages_as_read(request, id):
    try:
        user_ref = db.collection("users").document(id)
        user_data = user_ref.get().to_dict()
        if not user_data:
            return JsonResponse({"error": "User not found"}, status=404)
        
        inbox = user_data.get("inbox", [])
        for message in inbox:
            message["read"] = True
        user_ref.update({"inbox": inbox})
        return JsonResponse({"message": "All messages marked as read"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
