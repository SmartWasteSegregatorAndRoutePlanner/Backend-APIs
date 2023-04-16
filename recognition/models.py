from django.db import models

labels_class_choices = [
    ('RECYCLABLE', 'recyclable'),
    ('NON-RECYCLABLE', 'non-recyclable'),
    ('E-WASTE', 'e-waste'),
]

class GarbageLabel(models.Model):
    label = models.CharField(max_length=255)
    label_class = models.CharField(max_length=100, choices=labels_class_choices, default=None)
    is_configured = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.label} - {self.label_class}'