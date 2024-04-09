from django.urls import path, include, re_path
from . import views
from . import middleware
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# from .pages import home
urlpatterns = [
    path("", include("pages.urls")),
    path("create_user/", views.create_user, name="create_user"),
    path("delete_user/<str:uid>/", views.delete_user, name="delete_user"),
    path(
        "ok/", middleware.TokenValidationMiddleware(
            middleware.AnotherMiddleware(
                views.ok
                ))
    ),  # this worked alright
 
]
