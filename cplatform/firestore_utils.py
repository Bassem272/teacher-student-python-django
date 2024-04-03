import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase Admin SDK
def get_firestore_client():
    # Check if the Firebase app has already been initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate("dragna272.json")
        firebase_admin.initialize_app(cred)

    return firestore.client()
