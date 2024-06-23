# # videos/firestore_admin_utils.py
import json
import logging
import uuid
from google.cloud import firestore
from django.http import JsonResponse, HttpResponseBadRequest

# logger = logging.getLogger(__name__)

# def get_firestore_client():
#     return firestore.Client()

# db = get_firestore_client()

# def add_video(video_data, grade_id):
#     video_id = f"video_{uuid.uuid4()}"
#     video_data["id"] = video_id
#     try:
#         db.collection(grade_id).document(video_id).set(video_data)
#         return {"message": "Video created successfully", "video_data": video_data}
#     except Exception as e:
#         return {"error": str(e)}

# def get_video(grade_id, video_id):
#     try:
#         doc_ref = db.collection(grade_id).document(video_id)
#         doc = doc_ref.get()
#         if doc.exists:
#             return {"video_data": doc.to_dict()}
#         else:
#             return {"error": "Video not found"}
#     except Exception as e:
#         return {"error": str(e)}

# def update_video(video_id, video_data, grade_id):
#     try:
#         doc_ref = db.collection(grade_id).document(video_id)
#         doc_ref.update(video_data)
#         return {"message": "Video updated successfully", "video_data": video_data}
#     except Exception as e:
#         return {"error": str(e)}

# def delete_video(video_id, grade_id):
#     try:
#         doc_ref = db.collection(grade_id).document(video_id)
#         doc_ref.delete()
#         return {"message": "Video deleted successfully"}
#     except Exception as e:
#         return {"error": str(e)}

# def get_all_videos(grade_id):
#     try:
#         videos = []
#         docs = db.collection(grade_id).get()
#         for doc in docs:
#             videos.append(doc.to_dict())
#         return {"videos": videos}
#     except Exception as e:
#         return {"error": str(e)}
from google.cloud import firestore

db = firestore.Client()

def get_all_videos(grade):
    try:
        videos = []
        docs = db.collection(grade).get()
        for doc in docs:
            video_data = doc.to_dict()
            video_data['id'] = doc.id  # Add document ID to video_data
            videos.append(video_data)
        return {"videos": videos}
    except Exception as e:
        return {"error": str(e)}

def add_video(video_data, grade):
    try:
        db.collection(grade).add(video_data)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def update_video(video_id, video_data, grade):
    try:
        db.collection(grade).document(video_id).set(video_data)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def delete_video(video_id, grade):
    try:
        db.collection(grade).document(video_id).delete()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def get_video(grade, video_id):
    try:
        doc_ref = db.collection(grade).document(video_id)
        doc = doc_ref.get()
        if doc.exists:
            video_data = doc.to_dict()
            return {"video_data": video_data}
        else:
            return {"error": f"Video with ID {video_id} not found in grade {grade}"}
    except Exception as e:
        return {"error": str(e)}

def get_all_grades(request):
    try:
        # Fetch all collections
        collections = db.collections()
        grades = [collection.id for collection in collections if 'grade' in collection.id]
        return {"grades": grades}
    except Exception as e:
        return {"error": str(e)}
