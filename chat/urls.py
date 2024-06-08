from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    # path("<str:room_name>/",views.room),
    path('create_message/',views.create_message),
    path('delete_message/<str:id>/',views.delete_message),
    path('update_message/<str:id>/',views.update_message),
    path('get_all_messages/<str:grade>/',views.get_all_messages),
    path('delete_all_messages/',views.delete_all_messages),
]