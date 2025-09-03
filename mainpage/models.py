from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class ComputerUser(models.Model):
    ACCESS_LEVEL_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Administrator'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Student ID")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number")
    course = models.CharField(max_length=100, verbose_name="Course/Program")
    address = models.TextField(verbose_name="Address")
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, default='student', verbose_name="Access Level")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Status")
    computer_station = models.CharField(max_length=50, blank=True, null=True, verbose_name="Computer Station")
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="Last Login")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "Computer User"
        verbose_name_plural = "Computer Users"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def update_last_login(self):
        # Use system local time for last login tracking
        self.last_login = datetime.now()
        self.save(update_fields=['last_login'])


class ComputerUnit(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in-use', 'In Use'),
        ('maintenance', 'Maintenance'),
        ('retired', 'Retired'),
    ]
    
    unit_id = models.CharField(max_length=20, unique=True, verbose_name="Unit ID")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "Computer Unit"
        verbose_name_plural = "Computer Units"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.unit_id} - {self.status}"


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('sign-in', 'Sign In'),
        ('sign-out', 'Sign Out'),
    ]

    user = models.ForeignKey(ComputerUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    student_id = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    computer_station = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self):
        base = f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.action}"
        who = self.full_name or (self.user.full_name if self.user else self.student_id) or 'Unknown User'
        where = f" @ {self.computer_station}" if self.computer_station else ''
        return f"{base}: {who}{where}"
