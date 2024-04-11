from django.urls import path, include, re_path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from middleware import StudentAccessMiddleware,AdminAccessMiddleware,TokenValidationMiddleware,AnotherMiddleware
# from .pages import home
urlpatterns = [
    path("delete_student/<str:uid>/", views.delete_student, name="delete_student"),
    path("get_student_by_id/<str:id>/", views.get_student_by_id, name="get_student"),
    path("get_student_by_email/", views.get_student_by_email, name="get_student"),
    path("update_student/<str:uid>/", views.update_student, name="update_student"),
    path("get_all_students/", views.get_all_students, name="get_all_students"),
    path("", include("pages.urls")),
    path(
        "ok/", TokenValidationMiddleware(
            AnotherMiddleware(
                views.ok
                ))
    ),  # this worked alright
 
]
