from django.urls import path, include, re_path
from . import views
from middleware import (
    TokenValidationMiddleware,
    AdminAccessMiddleware,
    AnotherMiddleware,
    VerifiedEmail,
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# from .pages import home
urlpatterns = [
    path("", include("pages.urls")),
    path("register/", views.register, name="register"),
    # path("get_user1/", views.get_user1, name="get_user1"),  # Added comma here
    # path("get_user1/<int:id>/", views.get_user1, name="get_user1"),  # Added comma here
    path("create_user/", views.create_user, name="create_user"),
    path("get_user2/<str:value>/", TokenValidationMiddleware(views.get_user2)),
    path("get_all_users/", TokenValidationMiddleware(views.get_all_users)),
    path("get_all_students/", TokenValidationMiddleware(views.get_all_students)),
    path("get_all_teachers/", TokenValidationMiddleware(views.get_all_teachers)),
    path("get_all_parents/", TokenValidationMiddleware(views.get_all_parents)),
    path("verify-email/", views.verify_email, name="verify_email"),
    path(
        "users/<str:id>/update_password/", views.update_password, name="update_password"
    ),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("delete_user/<str:id>/", TokenValidationMiddleware(views.delete_user)),
    path(
        "ok/",
        TokenValidationMiddleware(AnotherMiddleware(views.ok)),
    ),  # this worked alright
    path("reset_password_email/", VerifiedEmail(views.reset_password_email)),
    path("reset_password_form/", VerifiedEmail(views.reset_password_form)),
    path("reset_password_page/", views.reset_password_page, name="reset_password_page"),
]
# Apply TokenValidationMiddleware to the get_user2 view
# views.get_user2 = method_decorator(TokenValidationMiddleware)(views.get_user2)
