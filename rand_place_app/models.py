from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=15)
    intro = models.CharField(max_length=300, blank=True)
    areaCode = models.IntegerField()
    sigunguCode = models.IntegerField()

    def __str__(self):
        return self.name
