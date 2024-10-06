from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=10)
    academic_year = models.IntegerField()
    seats = models.IntegerField()
    is_quota_open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class QuotaRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"  