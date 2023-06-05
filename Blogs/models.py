from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    models.CharField(max_length=50)

    file = models.FileField(upload_to="posts/", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.user.username}'


class Block(models.Model):
    blocker = models.ForeignKey(UserProfile, related_name='blocker', on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(UserProfile, related_name='blocked_user', on_delete=models.CASCADE)
