from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("<str:room_name>/",views.room),
    path('create_message/',views.create_message)
]