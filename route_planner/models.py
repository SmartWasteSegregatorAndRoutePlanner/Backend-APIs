from django.db import models

class GarbageBinLocation(models.Model):
    name = models.CharField(max_length=50)
    garbage_weight = models.FloatField(default=0)
    latitude = models.FloatField(default=19.2991243)
    longitude = models.FloatField(default=72.8780597)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)