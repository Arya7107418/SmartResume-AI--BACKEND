# resume_analyzer/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    preferred_job_titles = models.TextField(blank=True)
    preferred_locations = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsed_text = models.TextField(blank=True)
    skills = models.JSONField(default=dict, blank=True)
    experience = models.JSONField(default=dict, blank=True)
    education = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s resume - {self.uploaded_at}"

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    url = models.URLField()
    posted_date = models.DateField()
    source = models.CharField(max_length=100)  # LinkedIn, Indeed, etc.
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} at {self.company}"

class JobMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    match_score = models.FloatField()
    skills_match = models.JSONField(default=dict)
    experience_match = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'job')
        
    def __str__(self):
        return f"{self.user.username} - {self.job.title} ({self.match_score}%)"
