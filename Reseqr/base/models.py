from django.db import models
import uuid
import os
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('avatars/', filename)


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    # ----------------------------------------------------
    #       THE FIX FOR THE REVERSE ACCESSOR CLASH
    # ----------------------------------------------------
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups', # <--- UNIQUE related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', # <--- UNIQUE related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    # ----------------------------------------------------

    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(
        upload_to=user_avatar_path,
        null=True,
        blank=True,
        default='avatars/avatar.svg'
    )

    USERNAME_FIELD = 'email'
    # 'email' is already set as USERNAME_FIELD, so we need to add 'username'
    # back to REQUIRED_FIELDS since AbstractUser requires it by default.
    REQUIRED_FIELDS = ['username'] # You may want to keep 'username' for admin panel login


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    link = models.URLField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='room_qr_codes/', null=True, blank=True)
    qr_rating = models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100) ])

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
