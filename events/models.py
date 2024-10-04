from django.db import models

class Format(models.Model):
    distance = models.CharField(max_length=100, unique=True)
    format = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.distance} - {self.format}"

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    link = models.URLField()
    city = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    formats = models.ManyToManyField(Format)

    def __str__(self):
        return self.name
