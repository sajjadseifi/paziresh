from django.db import models

class IdeologicalAssessment(models.Model):
    full_name = models.CharField(max_length=100)
    rank = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rank} {self.full_name}".strip()