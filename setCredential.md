Thank you for providing the directory listing. It appears that your `creds.json` file is located in `D:\teacher-student-python-django`. This file is needed to authenticate your application with Firebase.

Here are the steps you should follow to set up the environment variable and ensure that the `creds.json` file is properly used:

### Step 1: Set Environment Variable

Open Command Prompt and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your `creds.json` file. Run the following command:

```cmd
set GOOGLE_APPLICATION_CREDENTIALS=D:\teacher-student-python-django\creds.json
```

### Step 2: Modify `firestore_utils.py`

Ensure that your `firestore_utils.py` script correctly initializes Firebase using the environment variable:

```python
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
```

### Step 3: Verify Credentials File and Path

Ensure that the `creds.json` file is indeed located at `D:\teacher-student-python-django\creds.json`.

### Step 4: Run Your Django Application

Restart your Django development server:

```cmd
py manage.py runserver
```

### Additional Notes:

- **Environment Variables:** Setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is crucial for authentication.
- **Security:** Make sure to keep your `creds.json` file secure and do not expose it in your source code repository.
- **Project ID:** Ensure that the project ID in your `creds.json` file matches the Firebase project ID you are using.

### Troubleshooting Tips:

- **Authentication Issues:** If you encounter authentication issues, ensure that your `creds.json` file is correctly formatted and valid.
- **Project ID Mismatch:** Verify that the project ID in your `creds.json` file matches the Firebase project ID you are using.

By following these steps, you should be able to resolve the issue and successfully authenticate with Firebase in your Django application. If you encounter any further issues, feel free to ask!