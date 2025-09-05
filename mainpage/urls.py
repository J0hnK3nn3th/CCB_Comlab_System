from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_old_admin(request):
    """Redirect old admin URL to new login page"""
    return redirect('login')

urlpatterns = [
    # Redirect old admin URL
    path('admins/', redirect_old_admin, name='old_admin_redirect'),
    
    # New admin URLs
    path('admin/login/', views.login_view, name='login'),
    path('admin/logout/', views.logout_view, name='logout'),
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('admin/computer_users/', views.computer_users, name='computer_users'),
    path('admin/computer_units/', views.computer_units, name='computer_units'),
    path('admin/computer_users/add/', views.add_user, name='add_user'),
    path('admin/computer_users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/computer_users/view/<int:user_id>/', views.view_user_details, name='view_user_details'),
    path('admin/computer_units/add/', views.add_computer_unit, name='add_computer_unit'),
    path('admin/computer_units/edit/<int:unit_id>/', views.edit_computer_unit, name='edit_computer_unit'),
    path('admin/logs/', views.logs_view, name='logs'),
    
    # API endpoints
    path('api/users/', views.get_users, name='api_get_users'),
    path('api/users/create/', views.create_user, name='api_create_user'),
    path('api/users/<int:user_id>/update/', views.update_user, name='api_update_user'),
    path('api/users/<int:user_id>/delete/', views.delete_user, name='api_delete_user'),
    path('api/users/<int:user_id>/status/', views.update_user_status, name='api_update_user_status'),
    
    # Student sign-in (public)
    path('', views.user_sign_in, name='user_sign_in'),
]
