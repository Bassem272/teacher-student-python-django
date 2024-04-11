
from django.urls import path

from .views import (
    get_inbox,
    get_notifications,
    send_message,
    mark_message_as_read,
    delete_message,
    clear_inbox,
    mark_all_messages_as_read,
)

urlpatterns = [
    path('inbox/<str:id>/', get_inbox, name='get_inbox'),
    path('notifications/<str:id>/', get_notifications, name='get_notifications'),
    path('send_message/<str:sender_id>/<str:receiver_id>/', send_message, name='send_message'),
    path('mark_message_as_read/<str:id>/<int:message_index>/', mark_message_as_read, name='mark_message_as_read'),
    path('delete_message/<str:user_id>/<int:message_index>/', delete_message, name='delete_message'),
    path('clear_inbox/<str:user_id>/', clear_inbox, name='clear_inbox'),
    path('mark_all_messages_as_read/<str:user_id>/', mark_all_messages_as_read, name='mark_all_messages_as_read'),
]