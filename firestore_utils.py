# # firestore_utils.py

# import firebase_admin
# from firebase_admin import credentials, firestore
# import os
# import logging

# def get_firestore_client():
#     try:
#         # Check if Firebase app is not already initialized
#         if not firebase_admin._apps:
#             # Initialize Firebase App with environment variable
#             cred = credentials.ApplicationDefault()
#             firebase_admin.initialize_app(cred, {
#                 'projectId': os.getenv('GOOGLE_CLOUD_PROJECT'),
#             })
#             logging.info('Firestore initialized successfully')

#         # Return Firestore client
#         return firestore.client()

#     except Exception as e:
#         logging.error(f'Error initializing Firestore: {str(e)}')
#         raise  # Re-raise the exception to propagate it further
import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_firestore_client():
    try:
        # Check for required environment variables
        cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        bucket_storage = os.getenv('BUCKET_STORAGE')
        if not cred_path or not project_id:
            raise EnvironmentError('GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT environment variable not set')

        # Check if Firebase app is not already initialized
        if not firebase_admin._apps:
            # Initialize Firebase App with environment variable
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
                'projectId': project_id,
                'storageBucket':
                'dragna272.appspot.com'
            })
            logging.info('Firestore initialized successfully')

        # Return Firestore client
        return firestore.client() , storage.bucket()

    except Exception as e:
        logging.error(f'Error initializing Firestore: {str(e)}')
        raise  # Re-raise the exception to propagate it further
