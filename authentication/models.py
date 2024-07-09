from django.db import models

class FirestoreUser(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Firestore User"
        verbose_name_plural = "Firestore Users"
