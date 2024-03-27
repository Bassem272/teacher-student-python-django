# firestore_utils.py

from firebase_admin import firestore

def get_firestore_client():
    return firestore.client()
