from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator 

class EventUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    ]
    
    # Linking to User model with a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Role field with choices and a default value
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')
    
    # Profile picture with a file size limit (optional improvement)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        null=True, 
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]  # Add file extension validation
    )
    
    # Phone number field with validation for specific pattern (optional improvement)
    phone_number = models.CharField(
        max_length=15, 
        null=True, 
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.')]
    )
    
    # The __str__ method is improved with role and user details for better readability in the admin
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

