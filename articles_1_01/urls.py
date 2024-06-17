from django.urls import path
from . import views

urlpatterns = [
    path('create_article/', views.create_article, name='create_article'),
    path('<str:article_id>/', views.get_article, name='get_article'),   
    # path('create/', views.create),   
    path('', views.get_all_articles, name='get_all_articles'),
  

]