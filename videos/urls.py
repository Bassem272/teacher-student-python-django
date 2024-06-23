# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.hello_world, name='videos_hello_world'),
#     # try to avoid conflicts in the urls ok and this is better than the other one ok 
#     path('create/<str:grade_id>/', views.create_video, name='create_video'),   
#     path('list/<str:grade_id>/', views.get_all_videos, name='get_all_videos'),
#     path('<str:grade_id>/<str:video_id>/', views.get_video, name='get_video'), 
#     path('collections/', views.get_all_grades, name='get_all_grades'),

# ]

from django.urls import path
from . import views
from .admin import FirestoreVideoAdmin

urlpatterns = [
    path('', views.hello_world, name='videos_hello_world'),
    path('create/<str:grade_id>/', views.create_video, name='create_video'),   
    path('list/<str:grade_id>/', views.get_all_videos, name='get_all_videos'),
    path('<str:grade_id>/<str:video_id>/', views.get_video, name='get_video'), 
    path('collections/', views.get_all_grades, name='get_all_grades'),
    # Custom admin views
    # path('admin/firestore_videos/', FirestoreVideoAdmin().changelist_view, name='admin_videos_changelist'),
    # path('admin/firestore_videos/add/', FirestoreVideoAdmin().add_view, name='admin_videos_add'),
    # path('admin/firestore_videos/<str:video_id>/change/', FirestoreVideoAdmin().change_view, name='admin_videos_change'),
    # path('admin/firestore_videos/<str:video_id>/delete/', FirestoreVideoAdmin().delete_view, name='admin_videos_delete'),
]
