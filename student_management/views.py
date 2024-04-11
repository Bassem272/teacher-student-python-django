from telnetlib import STATUS
from django.shortcuts import render
from grpc import Status
from requests import Response

from firestore_utils import get_firestore_client
from rest_framework.decorators import api_view
# Connection to the firestore
db = get_firestore_client()
# Create your views here.
@api_view(['GET'])
def get_all_students(request):

    students_ref = db.collection('users').where('role', '==', 'student').stream()
    students = []
    for student_ref in students_ref:
        student = student_ref.to_dict()
        student['id'] = student_ref.id
        students.append(student)
        
    return Response(students)

@api_view(['GET'])
def get_student_by_id(request, id):
    
    student_ref = db.collection('users').document(id)
    student = student_ref.get().to_dict()
    student['id'] = student_ref.id
    
    return Response(student)

@api_view(['GET'])
def get_student_by_email(request):
    
    email = request.query_params.get('email', None)
    if email is None:
        return Response({'error': 'Email parameter is required'}, status=STATUS.HTTP_400_BAD_REQUEST)
    student_ref = db.collection('users').where('email', '==', email).limit(1).stream()
    if not student_ref:
        return Response({'error': 'Student not found'}, status=Status.HTTP_404_NOT_FOUND)
    
    student = student_ref[0].to_dict()
    student['id'] = student_ref[0].id
    
    return Response(student)

@api_view(['DELETE'])
def delete_student(request, id):
    
    student_ref = db.collection('users').document(id)
    student_data = student_ref.get().to_dict()
    name = student_data['name']
    student_ref.delete()
    
    return Response({'message': f'Student {name}deleted successfully'})

