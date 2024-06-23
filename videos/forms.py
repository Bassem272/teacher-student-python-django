# videos/forms.py
# videos/forms.py

from django import forms
from .models import FirestoreVideo

class VideoForm(forms.ModelForm):
    class Meta:
        model = FirestoreVideo
        fields = ['grade', 'video_id', 'title', 'description', 'video_url', 'tags']
