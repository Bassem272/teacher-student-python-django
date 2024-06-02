from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    # path("<str:room_name>/",views.room),
    path('create_article/',views.create_article),
    path('delete_article/<str:id>/',views.delete_article),
    path('update_article/<str:id>/',views.update_article),
    path('get_all_articles/',views.get_all_articles),
]