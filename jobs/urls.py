from django.urls import path
from . import views

urlpatterns = [
    path('create_job/', views.create_job, name='create_job'),
    path('<str:job_id>/', views.get_job, name='get_job'),   
    # path('create/', views.create),   
    path('', views.get_all_jobs, name='get_all_jobs'),
  

]