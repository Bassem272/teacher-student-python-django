from django.urls import path, include, re_path
from . import views
import middleware
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# from .pages import home
urlpatterns = [
    path("", include("pages.urls")),
    path("register/", views.register, name="register"),
    # path("get_user1/", views.get_user1, name="get_user1"),  # Added comma here
    # path("get_user1/<int:id>/", views.get_user1, name="get_user1"),  # Added comma here
    path("create_user/", views.create_user, name="create_user"),
    path(
        "get_user2/<str:value>/", views.get_user2, name="get_user2"
    ),  # Added comma here
    path("verify-email/", views.verify_email, name="verify_email"),
    path(
        "users/<str:id>/update_password/", views.update_password, name="update_password"
    ),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("delete_user/<str:uid>/", views.delete_user, name="delete_user"),
    path(
        "ok/",
        middleware.TokenValidationMiddleware(
        middleware.AnotherMiddleware(views.ok)),
    ),  # this worked alright
    path("reset_password_email/", middleware.VerifiedEmail(views.reset_password_email)),
    path("reset_password_form/", middleware.VerifiedEmail(views.reset_password_form)),
    path("reset_password_page/", views.reset_password_page, name="reset_password_page"),
]
