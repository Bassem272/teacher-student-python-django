# firestore_utils.py

import firebase_admin
from firebase_admin import credentials, firestore
import os
import logging

def get_firestore_client():
    try:
        # Check if Firebase app is not already initialized
        if not firebase_admin._apps:
            # Initialize Firebase App with environment variable
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
                'projectId': os.getenv('GOOGLE_CLOUD_PROJECT'),
            })
            logging.info('Firestore initialized successfully')

        # Return Firestore client
        return firestore.client()

    except Exception as e:
        logging.error(f'Error initializing Firestore: {str(e)}')
        raise  # Re-raise the exception to propagate it further
