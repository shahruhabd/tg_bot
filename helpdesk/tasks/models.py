from django.db import models

class Task(models.Model):
    description = models.TextField()
    classroom = models.CharField(max_length=10)

    

