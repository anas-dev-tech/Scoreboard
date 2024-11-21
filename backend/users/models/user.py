from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from core.constants import Role  

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    
    role = models.SmallIntegerField(choices=Role.choices, default=Role.TEACHER)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)

    force_change_password = models.BooleanField(default=False)

    first_name = models.CharField(max_length=30, blank=True)
    
    last_name = models.CharField(max_length=30, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return f"/users/{self.pk}/"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.email

    def is_teacher(self):
        return self.role == Role.TEACHER
