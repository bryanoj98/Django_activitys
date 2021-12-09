from django.db import models
from jsonfield import JSONField


# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    disabled_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=35)

    def __str__(self):
        return self.title


class Activity(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.PROTECT)
    schedule = models.DateTimeField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.CharField(max_length=35)

    def __str__(self):
        return self.title


class Survey(models.Model):
    activity_id = models.ForeignKey(Activity, on_delete=models.PROTECT)
    created_at = models.DateTimeField()
    answer = JSONField(default="")

