from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='videos_hello_world'),
    path('<str:grade_id>/<str:video_id>/', views.get_video),   
    path('<str:grade_id>/create_video/', views.create_video),   
    path('<str:grade_id>/', views.get_all_videos, name='get_all_videos'),

]