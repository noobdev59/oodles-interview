from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from phone_field import PhoneField
from django.conf import settings
from utils.models import Address, Friend

def profile_upload_image_handler(instance, filename):
    return instance.username+filename


class ProfileManager(BaseUserManager):
    def create_user(self, email, name, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Name is required during registration')
        if not phone_number:
            raise ValueError('Phone Number is required during registration')
        try:
            Profile.objects.get(phone_number=phone_number)
            raise ValueError('This phone number is already in use.')
        except Profile.DoesNotExist:
            pass

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_number, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            name,
            phone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    phone_number = PhoneField(unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=255)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    permanent_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='permanent_address', null=True, blank=True)
    company_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='company_address', null=True, blank=True)
    profile_picture = models.ImageField(upload_to=profile_upload_image_handler, null=True, blank=True)
    friends = models.ManyToManyField(Friend, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
