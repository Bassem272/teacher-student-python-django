from django.urls import path
from . import views

urlpatterns = [
    path('create_article/', views.create_article, name='create_article'),
    path('get_article/<str:article_id>/', views.get_article, name='get_article'),   
    # path('create/', views.create),   
    path('', views.get_all_articles, name='get_all_articles'),
    path('grades/', views.get_grades, name='get_grades'),
    path('grades/<str:grade>/subjects/', views.get_subjects, name='get_subjects'),
    path('grades/<str:grade>/subjects/<str:subject>/articles/', views.get_articles, name='get_articles'),
    path('grades/<str:grade>/subjects/<str:subject>/articles/<str:article_id>/', views.get_article, name='get_article'),
    path('create/grades/<str:grade>/subjects/<str:subject>/articles/', views.create_article_g, name='get_article'),
    path('recommended_articles/<str:grade>/', views.recommended_articles, name='recommended_articles'),
]