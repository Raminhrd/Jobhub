from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    remaining_capacity = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    @property
    def is_open(self):
        return self.start_date <= timezone.now() <= self.end_date and self.remaining_capacity > 0

    def decrease_capacity(self):
        if self.remaining_capacity > 0:
            self.remaining_capacity -= 1
            self.save()

    def __str__(self):
        return self.title


class Candidate(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15)
    education_level = models.CharField(max_length=50, choices=[
        ('b', 'Bachelor'),
        ('m', 'Master'),
        ('p', 'PhD')
    ])
    gpa = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(20.0)])
    job = models.ForeignKey(JobPosition, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class JobBasket(models.Model):
    candidate = models.ForeignKey(to=Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(to=JobPosition, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.first_name} - {self.job.title}"
