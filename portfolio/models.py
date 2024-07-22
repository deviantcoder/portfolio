from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Portfolio(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and Portfolio.objects.exists():
            return ValidationError('Portfolio already exists')
        super().save(*args, **kwargs)


class Skill(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    progress = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])


class Socials(models.Model):
    pass