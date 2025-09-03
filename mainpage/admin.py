from django.contrib import admin
from .models import ComputerUser, ComputerUnit, ActivityLog

# Register your models here.

@admin.register(ComputerUser)
class ComputerUserAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'email', 'course', 'access_level', 'status', 'computer_station', 'last_login', 'created_at')
    list_filter = ('access_level', 'status', 'course', 'created_at')
    search_fields = ('student_id', 'first_name', 'last_name', 'email', 'course')
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student_id', 'first_name', 'last_name', 'email', 'contact_number')
        }),
        ('Academic Information', {
            'fields': ('course', 'access_level')
        }),
        ('Status & Access', {
            'fields': ('status', 'computer_station', 'last_login')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(ComputerUnit)
class ComputerUnitAdmin(admin.ModelAdmin):
    list_display = ('unit_id', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('unit_id',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Unit Information', {
            'fields': ('unit_id', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action', 'student_id', 'full_name', 'computer_station', 'user')
    list_filter = ('action', 'computer_station', 'timestamp')
    search_fields = ('student_id', 'full_name', 'computer_station', 'notes')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
