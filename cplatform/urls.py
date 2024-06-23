"""
URL configuration for cplatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from videos.admin import firestore_video_admin
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from videos.admin import FirestoreVideoAdmin
from videos.models import FirestoreVideo

# Instantiate FirestoreVideoAdmin with model and admin_site
# firestore_video_admin = FirestoreVideoAdmin(FirestoreVideo, admin.site)
# from videos.admin import firestore_admin_site
from videos.admin import FirestoreVideoAdmin

# Instantiate the FirestoreVideoAdmin class
firestore_video_admin_instance = FirestoreVideoAdmin(model=FirestoreVideo, admin_site=admin.site)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("videos/", include("videos.urls")), 
    path("auth/", include("authentication.urls")),
    path('firestore_admin/', include(firestore_video_admin_instance.get_urls())),  # Correctly include the admin URLs
    path("chat/", include("chat.urls")),
    # path("articles/", include("articles.urls")),
    path("jobs/", include("jobs.urls")), 
    path("articles/", include("articles_1_01.urls")), 
    
    # path("", include("pages.urls")),
    # path("projects/", include("projects.urls")),
    # path("communication/", include("messaging_and_communication.urls")),
    # path('ws/', include(cplatform.routing.websocket_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
