from firestore_utils import get_firestore_client

# Connection to the firestore
db = get_firestore_client()

def add_user(user_data):
    try:
        db.collection('users').document(user_data['user_id']).set(user_data)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def get_user(user_id):
    try:
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return {"user_data": doc.to_dict()}
        else:
            return {"error": f"User with ID {user_id} not found"}
    except Exception as e:
        return {"error": str(e)}

def update_user(user_id, user_data):
    try:
        db.collection('users').document(user_id).set(user_data)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def delete_user(user_id):
    try:
        db.collection('users').document(user_id).delete()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def get_all_users():
    try:
        users = []
        docs = db.collection('users').get()
        print(docs)
        for doc in docs:
            user_data = doc.to_dict()
            user_data['id'] = doc.id  # Add document ID to user_data
            users.append(user_data)
        return {"users": users}
    except Exception as e:
        return {"error": str(e)}
