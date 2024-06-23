
from django.contrib import admin
from django.shortcuts import redirect
from .models import FirestoreVideo
from .forms import VideoForm
from .firestore_admin_utils import get_all_videos, add_video, update_video, delete_video, get_video, get_all_grades
from django.urls import path
from django.shortcuts import render

class FirestoreVideoAdmin(admin.ModelAdmin):
    change_list_template = 'admin/firestore_change_list.html'
    add_form_template = 'admin/firestore_add_form.html'
    change_form_template = 'admin/firestore_change_form.html'
    form = VideoForm

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(self.add_view), name='videos_videoform_add'),
            path('<str:grade>/<str:video_id>/change/', self.admin_site.admin_view(self.change_view), name='videos_videoform_change'),
            path('<str:grade>/<str:video_id>/delete/', self.admin_site.admin_view(self.delete_view), name='videos_videoform_delete'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        grade = request.GET.get('grade', 'grade1')  # Default to grade1 if not provided
        videos_response = get_all_videos(grade)
        videos = videos_response.get("videos", [])

        # Fetch all grades
        grades_response = get_all_grades(request)
        grades = grades_response.get("grades", [])

        # Prepare the context
        context = {
            'videos': videos,
            'grade': grade,
            'grades': grades,
        }

        return render(request, self.change_list_template, context)

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'POST':
            form = VideoForm(request.POST)
            if form.is_valid():
                video_data = {
                    "grade": form.cleaned_data['grade'],
                    "title": form.cleaned_data['title'],
                    "description": form.cleaned_data['description'],
                    "video_url": form.cleaned_data['video_url'],
                    "tags": form.cleaned_data['tags'].split(','),
                }
                result = add_video(video_data, form.cleaned_data['grade'])
                if 'error' not in result:
                    self.message_user(request, "Video added successfully.")
                    return self.changelist_view(request)
                else:
                    self.message_user(request, result['error'], level='error')
        else:
            form = VideoForm()

        return render(request, self.add_form_template, {'form': form})

    def change_view(self, request, grade, video_id, form_url='', extra_context=None):
        if request.method == 'POST':
            form = VideoForm(request.POST)
            if form.is_valid():
                video_data = {
                    "grade": form.cleaned_data['grade'],
                    "title": form.cleaned_data['title'],
                    "description": form.cleaned_data['description'],
                    "video_url": form.cleaned_data['video_url'],
                    "tags": form.cleaned_data['tags'].split(','),
                }
                result = update_video(video_id, video_data, grade)
                if 'error' not in result:
                    self.message_user(request, "Video updated successfully.")
                    return redirect('admin:videos_videoform_change', grade=grade, video_id=video_id)
                else:
                    self.message_user(request, result['error'], level='error')
        else:
            video = get_video(grade, video_id).get("video_data", {})
            initial_data = {
                'grade': video.get('grade', ''),
                'title': video.get('title', ''),
                'description': video.get('description', ''),
                'video_url': video.get('video_url', ''),
                'tags': ','.join(video.get('tags', [])),
            }
            form = VideoForm(initial=initial_data)

        return render(request, self.change_form_template, {'form': form, 'video_id': video_id})

    def delete_view(self, request, grade, video_id, form_url='', extra_context=None):
        result = delete_video(video_id, grade)
        if 'error' not in result:
            self.message_user(request, "Video deleted successfully.")
        else:
            self.message_user(request, result['error'], level='error')
        return self.changelist_view(request)

# Register the admin site
admin.site.register(FirestoreVideo, FirestoreVideoAdmin)
