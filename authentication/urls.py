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
from .article_views import *
from .channel_views import *
# from .pages import home
urlpatterns = [
    path("", include("pages.urls")),
    path("register/", views.register, name="register"),
    # path("get_user1/", views.get_user1, name="get_user1"),  # Added comma here
    # path("get_user1/<int:id>/", views.get_user1, name="get_user1"),  # Added comma here
    path("create_user/", views.create_user, name="create_user"),
    path("verify-email/", views.verify_email, name="verify_email"),
    path("get_user2/<str:value>/", TokenValidationMiddleware(views.get_user2)),
    path("get_all_users/", TokenValidationMiddleware(views.get_all_users)),
    path("get_all_students/", TokenValidationMiddleware(views.get_all_students)),
    path("get_all_teachers/", TokenValidationMiddleware(views.get_all_teachers)),
    path("get_all_parents/", TokenValidationMiddleware(views.get_all_parents)),
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
    # Article URLs
    path('article/create/', create_article, name='create_article'),
    path('article/<str:article_id>/', get_article_by_id, name='get_article_by_id'),
    path('article/update/<str:article_id>/', update_article, name='update_article'),
    path('article/delete/<str:article_id>/', delete_article, name='delete_article'),
    path('article/', get_all_articles, name='get_all_articles'),  # New endpoint
    # Channel URLs
    path('channel/create/', create_channel, name='create_channel'),
    path('channel/<str:channel_id>/', get_channel_by_id, name='get_channel_by_id'),
    path('channel/update/<str:channel_id>/', update_channel, name='update_channel'),
    path('channel/delete/<str:channel_id>/', delete_channel, name='delete_channel'),
    path('channel/', get_all_channels, name='get_all_channels'),  # New endpoint
    # Subscription endpoints
    path('channel/subscribe/<str:channel_id>/', subscribe_to_channel, name='subscribe_to_channel'),
    path('channel/unsubscribe/<str:channel_id>/', unsubscribe_from_channel, name='unsubscribe_from_channel'),
    path('channel/<str:channel_id>/messages/send/', send_message, name='send_message'),
    path('channel/<str:channel_id>/messages/', get_messages, name='get_channel_messages'),
    path('channel/<str:channel_id>/messages/<str:message_id>/edit/', edit_message, name='edit_message'),
    path('channel/<str:channel_id>/messages/<str:message_id>/delete/', delete_message, name='delete_message'),
]
# Apply TokenValidationMiddleware to the get_user2 view
# views.get_user2 = method_decorator(TokenValidationMiddleware)(views.get_user2)
