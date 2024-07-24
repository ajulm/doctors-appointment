from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


from django.conf import settings
from django.core.mail import send_mail

# Create your models here.
GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Others"),
)

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, username=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        # user.save(commit=False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        # extra_fields.setdefault("role", "admin")
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(
            email=email, password=password, username=username, **extra_fields
        )

    def is_not_deleted(self):
        return self.filter(is_deleted=False)

    def active(self):
        return self.filter(is_deleted=False, status=True)


ROLE_CHOICES = (
    ("doctor", "Doctor"),
    ("admin", "Admin"),
)


class CustomUser(AbstractUser, models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=False, blank=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default="user")

    is_email_notification_preferred = models.BooleanField(default=True)
    is_sms_notification_preferred = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Doctor"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()
        super().save(*args, **kwargs)

    def generate_username(self):
        short_uuid = str(uuid.uuid4())  # Get the first 8 characters of UUID
        return short_uuid


APPOINTMENT_CHOICES_DICT = {
    'physician': 'Physician',
    'neurologist': 'Neurologist',
    'psychiatrist': 'Psychiatrist',
    'oncologist': 'Oncologist',
    'dentist': 'Dentist',
    'pediatrician': 'Pediatrician',
    'gynecologist': 'Gynecologist',
}
APPOINTMENT_CHOICES = list(APPOINTMENT_CHOICES_DICT.items())


class Appointment(models.Model):  
    type = models.CharField(choices=APPOINTMENT_CHOICES, max_length=255)
    appointment_id = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    verified_at = models.DateTimeField(null=True, blank=True)
    scheduled_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.appointment_id

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            self.appointment_id = str(uuid.uuid4())
        if not self.code:
            self.code = str(uuid.uuid4())[:6]
        if self.customer_email:
            self.send_email()
        super().save(*args, **kwargs)

    def send_email(self):
        subject = 'Welcome to HealthEase'
        message = f"""Hi {self.name}, \n\nYour code is {self.code} \n\nThank you for registering your appointment."""
        email_from = "admin@virtucare.com"
        recipient_list = [self.customer_email, ]
        send_mail(subject, message, email_from, recipient_list )
        return
