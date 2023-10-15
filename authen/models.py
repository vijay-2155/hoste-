from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
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

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    college = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(null=True)

    PROFILE_CHOICES = (
        ('owner', 'Owner'),
        ('student', 'Student'),
    )
    profile_type = models.CharField(max_length=7, choices=PROFILE_CHOICES, default='student')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Location(models.Model):
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.city}, {self.state},{self.message}"


class RentalInformation(models.Model):
    name = models.CharField(max_length=100)
    rental_type = models.CharField(max_length=20, choices=[
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('other', 'Other'),
    ])
    water_facilities = models.BooleanField(default=False)
    electricity = models.BooleanField(default=False)
    proximity_to_grocery_stores = models.BooleanField(default=False)
    nearest_transportation = models.CharField(max_length=10, choices=[
        ('bus', 'Bus'),
        ('train', 'Train'),
    ])
    max_people = models.PositiveIntegerField()
    num_rooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    extra_info = models.TextField()
    owner_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    has_whatsapp = models.BooleanField(default=False)
    email = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)

    def __str__(self):
        return self.name


class HostelInformation(models.Model):
    name = models.CharField(max_length=100)
    hostel_type = models.CharField(max_length=20, choices=[
        ('Boys', 'Boys'),
        ('Ladies', 'Ladies'),
    ])
    water_facilities = models.BooleanField(default=False)
    image = models.ImageField(upload_to='hostel_images/', blank=True, null=True)  # Use ImageField for images
    wifi = models.BooleanField(default=False)
    proximity_to_grocery_stores = models.BooleanField(default=False)
    nearest_transportation = models.CharField(max_length=10, choices=[
        ('bus', 'Bus'),
        ('train', 'Train'),
    ])
    room_type = models.CharField(max_length=20, choices=[
        ('Individual', 'Individual'),
        ('Halltype', 'Hall-type'),
    ])
    max_people = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    extra_info = models.TextField()
    owner_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    has_whatsapp = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    email = models.EmailField()

    def __str__(self):
        return self.name
