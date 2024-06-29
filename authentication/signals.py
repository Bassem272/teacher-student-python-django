# authentication/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from google.cloud import firestore
import datetime

db = firestore.Client()

@receiver(post_save, sender=User)
def create_user_in_firestore(sender, instance, created, **kwargs):
    print(f"{instance.first_name} {instance.last_name}", instance.email)
    # name =f"{instance.first_name} {instance.last_name}"
    if created:
        datao = {
            "user_id": instance.id,
            "credits": 0,
            "email": instance.email,
            "name": instance.first_name,
            "avatar_url": "photo_url",
            "password": instance.password,  # Hashed password
            "email_verified": instance.is_active,
            "verification_code": "",
            "age": 18,
            "country": "country",
            "mobile": "mobile",
            "lastLogin": datetime.datetime.now(),
            "grade": "grade",
            "contacts": [],
            "token": "jwtToken",
            "role": "role",  # You can set this based on your logic
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
            "push_notifications_enabled": True
        }
        
        user_ref = db.collection("users").document(str(instance.id))
        user_ref.set(datao)
