from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
import json
from datetime import datetime
from .models import ComputerUser, ComputerUnit, ActivityLog
from django.db import models

# Create your views here.
def dashboard(request):
    total_users = ComputerUser.objects.count()
    total_units = ComputerUnit.objects.count()
    available_units = ComputerUnit.objects.filter(status='available').count()
    occupied_units = ComputerUnit.objects.filter(status='in-use').count()
    maintenance_units = ComputerUnit.objects.filter(status='maintenance').count()
    available_units_list = ComputerUnit.objects.filter(status='available').order_by('unit_id')
    occupied_units_list = ComputerUnit.objects.filter(status='in-use').order_by('unit_id')
    maintenance_units_list = ComputerUnit.objects.filter(status='maintenance').order_by('unit_id')
    context = {
        'total_users': total_users,
        'total_units': total_units,
        'available_units': available_units,
        'occupied_units': occupied_units,
        'maintenance_units': maintenance_units,
        'available_units_list': available_units_list,
        'occupied_units_list': occupied_units_list,
        'maintenance_units_list': maintenance_units_list,
        'current_page': 'dashboard',
    }
    return render(request, 'dashboard.html', context)

def computer_users(request):
    # Get all users for display
    users = ComputerUser.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'total_users': users.count(),
        'active_users': users.filter(status='active').count(),
        'all_users': users,  # Add this for the template to use
        'current_page': 'computer_users',
    }
    return render(request, 'computer_users.html', context)

def computer_units(request):
    # Get all computer units for display
    units = ComputerUnit.objects.all().order_by('-created_at')
    
    context = {
        'units': units,
        'total_units': units.count(),
        'available_units': units.filter(status='available').count(),
        'current_page': 'computer_units',
    }
    return render(request, 'computer_units.html', context)

def add_user(request):
    """Handle form submission to add a new user"""
    if request.method == 'POST':
        try:
            # Get form data
            student_id = request.POST.get('student_id')
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            email = request.POST.get('email')
            contact_number = request.POST.get('contactNumber')
            course = request.POST.get('course')
            address = request.POST.get('address')
            
            # Validate required fields
            if not all([student_id, first_name, last_name, contact_number, course, address]):
                messages.error(request, 'All required fields must be filled.')
                return redirect('computer_users')
            
            # Check if student ID already exists
            if ComputerUser.objects.filter(student_id=student_id).exists():
                messages.error(request, 'Student ID already exists.')
                return redirect('computer_users')
            
            # Create user
            user = ComputerUser.objects.create(
                student_id=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email if email else '',
                contact_number=contact_number,
                course=course,
                address=address,
                access_level='student',  # Default access level
                status='active',  # Default status
                computer_station='',  # Default empty station
            )
            
            messages.success(request, f'User {user.full_name} added successfully!')
            return redirect('computer_users')
            
        except Exception as e:
            messages.error(request, f'Error adding user: {str(e)}')
            return redirect('computer_users')
    
    # If GET request, redirect to computer users page
    return redirect('computer_users')

def edit_user(request, user_id):
    """Handle form submission to edit an existing user"""
    user = get_object_or_404(ComputerUser, id=user_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            email = request.POST.get('email')
            contact_number = request.POST.get('contactNumber')
            course = request.POST.get('course')
            address = request.POST.get('address')
            access_level = request.POST.get('access_level')
            status = request.POST.get('status')
            computer_station = request.POST.get('computer_station')
            
            # Update user fields
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email is not None:
                user.email = email
            if contact_number:
                user.contact_number = contact_number
            if course:
                user.course = course
            if address:
                user.address = address
            if access_level:
                user.access_level = access_level
            if status:
                user.status = status
            if computer_station is not None:
                user.computer_station = computer_station
            
            user.save()
            messages.success(request, f'User {user.full_name} updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    return redirect('computer_users')

def view_user_details(request, user_id):
    """Display user details in a modal"""
    if request.method == 'GET':
        try:
            user = get_object_or_404(ComputerUser, id=user_id)
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'student_id': user.student_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'full_name': user.full_name,
                    'email': user.email,
                    'contact_number': user.contact_number,
                    'course': user.course,
                    'address': user.address,
                    'access_level': user.access_level,
                    'status': user.status,
                    'computer_station': user.computer_station or 'Not Assigned',
                    'last_login': user.last_login.strftime('%B %d, %Y at %I:%M %p') if user.last_login else 'Never',
                    'created_at': user.created_at.strftime('%B %d, %Y at %I:%M %p'),
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error retrieving user details: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def add_computer_unit(request):
    """Handle form submission to add a new computer unit"""
    if request.method == 'POST':
        try:
            # Get form data
            unit_id = request.POST.get('unitId')
            status = request.POST.get('status')
            
            # Validate required fields
            if not all([unit_id, status]):
                messages.error(request, 'Unit ID and Status are required fields.')
                return redirect('computer_units')
            
            # Check if unit ID already exists
            if ComputerUnit.objects.filter(unit_id=unit_id).exists():
                messages.error(request, 'Unit ID already exists.')
                return redirect('computer_units')
            
            # Create computer unit
            unit = ComputerUnit.objects.create(
                unit_id=unit_id,
                status=status,
            )
            
            messages.success(request, f'Computer unit {unit.unit_id} added successfully!')
            return redirect('computer_units')
            
        except Exception as e:
            messages.error(request, f'Error adding computer unit: {str(e)}')
            return redirect('computer_units')
    
    # If GET request, redirect to computer units page
    return redirect('computer_units')


def edit_computer_unit(request, unit_id):
    """Handle form submission to edit an existing computer unit"""
    unit = get_object_or_404(ComputerUnit, id=unit_id)
    if request.method == 'POST':
        try:
            new_unit_id = request.POST.get('unitId', '').strip()
            new_status = request.POST.get('status', '').strip()

            # Validate required fields
            if not new_unit_id or not new_status:
                messages.error(request, 'Unit ID and Status are required fields.')
                return redirect('computer_units')

            # If unit_id changed, ensure uniqueness
            if new_unit_id != unit.unit_id and ComputerUnit.objects.filter(unit_id=new_unit_id).exists():
                messages.error(request, 'Another unit with this Unit ID already exists.')
                return redirect('computer_units')

            unit.unit_id = new_unit_id
            unit.status = new_status
            unit.save()

            messages.success(request, f'Computer unit {unit.unit_id} updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating computer unit: {str(e)}')
    return redirect('computer_units')


def user_sign_in(request):
    """Public sign-in page where a user enters Student ID and selects an available PC"""
    available_units_qs = ComputerUnit.objects.filter(status='available').order_by('unit_id')
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        selected_unit_id = request.POST.get('unit_id', '').strip()

        if not student_id:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Student ID is required.'}, status=400)
            messages.error(request, 'Please enter your Student ID.')
            return redirect('user_sign_in')

        # Verify user exists
        try:
            user = ComputerUser.objects.get(student_id=student_id)
        except ComputerUser.DoesNotExist:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Student ID not found. Please contact the administrator to be registered.'}, status=404)
            messages.error(request, 'Student ID not found. Please contact the administrator to be registered.')
            return redirect('user_sign_in')

        # Step 1: If no unit provided yet, return available units list
        if not selected_unit_id:
            # If user is already signed in (has a computer_station), sign them out
            if user.computer_station:
                previous_unit_id = user.computer_station
                unit_obj = ComputerUnit.objects.filter(unit_id=previous_unit_id).first()
                if unit_obj:
                    unit_obj.status = 'available'
                    unit_obj.save(update_fields=['status'])
                user.computer_station = ''
                user.save(update_fields=['computer_station'])

                # Log sign-out
                ActivityLog.objects.create(
                    user=user,
                    student_id=user.student_id,
                    full_name=user.full_name,
                    action='sign-out',
                    computer_station=previous_unit_id,
                    notes='Signed out via kiosk form'
                )

                signout_message = f"Signed out successfully. PC {previous_unit_id} is now available."
                if is_ajax:
                    return JsonResponse({'success': True, 'message': signout_message, 'signed_out': True, 'unit_id': previous_unit_id})
                messages.success(request, signout_message)
                return redirect('user_sign_in')

            units = list(ComputerUnit.objects.filter(status='available').order_by('unit_id').values_list('unit_id', flat=True))
            if is_ajax:
                return JsonResponse({'success': True, 'units': units, 'student_name': user.full_name})
            messages.info(request, 'Please select a PC to proceed.')
            return redirect('user_sign_in')

        # Step 2: Verify unit is available and finalize sign-in
        try:
            unit = ComputerUnit.objects.get(unit_id=selected_unit_id, status='available')
        except ComputerUnit.DoesNotExist:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Selected PC is no longer available. Please pick another one.'}, status=409)
            messages.error(request, 'Selected PC is no longer available. Please pick another one.')
            return redirect('user_sign_in')

        # Assign the unit to the user and mark it in use
        unit.status = 'in-use'
        unit.save(update_fields=['status'])

        user.computer_station = unit.unit_id
        # Use system local time for last login tracking
        user.last_login = datetime.now()
        user.save(update_fields=['computer_station', 'last_login'])

        # Log sign-in
        ActivityLog.objects.create(
            user=user,
            student_id=user.student_id,
            full_name=user.full_name,
            action='sign-in',
            computer_station=unit.unit_id,
            notes=f'Signed in via kiosk form - Last login updated to {datetime.now().strftime("%B %d, %Y at %I:%M %p")}'
        )

        success_message = f"Signed in successfully. Proceed to PC {unit.unit_id}."
        if is_ajax:
            return JsonResponse({'success': True, 'message': success_message, 'unit_id': unit.unit_id})

        messages.success(request, success_message)
        return redirect('user_sign_in')

    context = {
        'available_units': available_units_qs,
    }
    return render(request, 'userpage.html', context)

def logs_view(request):
    logs = ActivityLog.objects.select_related('user').all().order_by('-timestamp')
    # Optional pagination similar to users page
    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'logs': page_obj,
        'all_logs': logs,
        'current_page': 'logs',
    }
    return render(request, 'logs.html', context)

# API Views for Computer Users
@csrf_exempt
@require_http_methods(["GET"])
def get_users(request):
    """Get all users or search users"""
    search_query = request.GET.get('search', '')
    
    if search_query:
        users = ComputerUser.objects.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(student_id__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(course__icontains=search_query)
        )
    else:
        users = ComputerUser.objects.all()
    
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'student_id': user.student_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'email': user.email,
            'contact_number': user.contact_number,
            'course': user.course,
            'address': user.address,
            'access_level': user.access_level,
            'status': user.status,
            'computer_station': user.computer_station,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat(),
        })
    
    return JsonResponse({'users': users_data, 'total': len(users_data)})

@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    """Create a new user"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['student_id', 'first_name', 'last_name', 'contact_number', 'course', 'address']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'{field.replace("_", " ").title()} is required'
                }, status=400)
        
        # Check if student ID already exists
        if ComputerUser.objects.filter(student_id=data['student_id']).exists():
            return JsonResponse({
                'success': False,
                'error': 'Student ID already exists'
            }, status=400)
        
        # Create user
        user = ComputerUser.objects.create(
            student_id=data['student_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data.get('email', ''),
            contact_number=data['contact_number'],
            course=data['course'],
            address=data['address'],
            access_level=data.get('access_level', 'student'),
            status=data.get('status', 'active'),
            computer_station=data.get('computer_station', ''),
        )
        
        return JsonResponse({
            'success': True,
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'student_id': user.student_id,
                'full_name': user.full_name,
                'email': user.email,
                'course': user.course,
                'access_level': user.access_level,
                'status': user.status,
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_user(request, user_id):
    """Update an existing user"""
    try:
        user = get_object_or_404(ComputerUser, id=user_id)
        data = json.loads(request.body)
        
        # Update fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'contact_number' in data:
            user.contact_number = data['contact_number']
        if 'course' in data:
            user.course = data['course']
        if 'address' in data:
            user.address = data['address']
        if 'access_level' in data:
            user.access_level = data['access_level']
        if 'status' in data:
            user.status = data['status']
        if 'computer_station' in data:
            user.computer_station = data['computer_station']
        
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'student_id': user.student_id,
                'full_name': user.full_name,
                'email': user.email,
                'course': user.course,
                'access_level': user.access_level,
                'status': user.status,
                'computer_station': user.computer_station,
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    """Delete a user"""
    try:
        user = get_object_or_404(ComputerUser, id=user_id)
        user_name = user.full_name
        user.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'User {user_name} deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def update_user_status(request, user_id):
    """Update user status (active/inactive/suspended)"""
    try:
        user = get_object_or_404(ComputerUser, id=user_id)
        data = json.loads(request.body)
        
        if 'status' not in data:
            return JsonResponse({
                'success': False,
                'error': 'Status is required'
            }, status=400)
        
        user.status = data['status']
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': f'User status updated to {user.status}',
            'status': user.status
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)