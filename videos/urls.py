from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='videos_hello_world'),
    # path('<str:grade_id>/<str:video_id>/', views.get_video, name='get_video'),   
    # path('<str:grade_id>/', views.create_video, name='create_video'),   
    # path('<str:grade_id>/list/', views.get_all_videos, name='get_all_videos'),
    
    # try to avoid conflicts in the urls ok and this is better than the other one ok 
    path('create/<str:grade_id>/', views.create_video, name='create_video'),   
    path('list/<str:grade_id>/', views.get_all_videos, name='get_all_videos'),
    path('<str:grade_id>/<str:video_id>/', views.get_video, name='get_video'), 

]