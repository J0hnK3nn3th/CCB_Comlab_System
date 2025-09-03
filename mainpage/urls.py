from django.urls import path
from . import views

urlpatterns = [
    path('admins', views.dashboard, name='dashboard'),
    path('computer_users/', views.computer_users, name='computer_users'),
    path('computer_units/', views.computer_units, name='computer_units'),
    path('computer_users/add/', views.add_user, name='add_user'),
    path('computer_users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('computer_users/view/<int:user_id>/', views.view_user_details, name='view_user_details'),
    path('computer_units/add/', views.add_computer_unit, name='add_computer_unit'),
    path('computer_units/edit/<int:unit_id>/', views.edit_computer_unit, name='edit_computer_unit'),
    path('', views.user_sign_in, name='user_sign_in'),
    path('logs/', views.logs_view, name='logs'),
]
