from django.db import models
from django.contrib.auth.models import User


class ToDo(models.Model):
    TYPE_STATUS = (
        ('f', 'fun'),
        ('l', 'low'),
        ('m', 'middle'),
        ('e', 'emergency'),
    )
    STAGE_STATUS = (
        ('d', 'defined'),
        ('p', 'progressing'),
        ('c', 'complete'),
    )

    type = models.CharField(
        max_length=1,
        choices=TYPE_STATUS,
    )
    stage = models.CharField(
        max_length=1,
        choices=STAGE_STATUS,
        default='d'
    )
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    done_time = models.DateTimeField(null=True, blank=True)
    point = models.IntegerField()

    def __str__(self):
        return self.title


class Activity(models.Model):
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="activity_user"
    )

    def __str__(self):
        return self.user.username


class Gift(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Awards(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)


class Pause(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class TaskPause(models.Model):
    task = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.task.title
