from django.db import models


# Create your models here.
class PersonsCount(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()
