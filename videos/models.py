# videos/models.py

# from django.db import models

# class FirestoreVideo(models.Model):
#     grade_id = models.CharField(max_length=50)
#     video_id = models.CharField(max_length=50)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     video_url = models.URLField()
#     tags = models.CharField(max_length=200)

#     def __str__(self):
#         return self.title

from django.db import models

class FirestoreVideo(models.Model):
    # Define your model fields here
    grade = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()
    video_id = models.CharField(max_length=50)
    tags = models.CharField(max_length=255)

    def __str__(self):
        return self.title  # Example: Return a readable representation of the object

