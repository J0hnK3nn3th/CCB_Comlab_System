# ComLab System - Database Storage Without APIs

This Django project demonstrates how to store data in a database without using API endpoints. Instead, it uses traditional Django form submissions and views.

## Features

- **Add Users**: Add new computer lab users through a modal form
- **Edit Users**: Edit existing user information through individual edit modals
- **View User Details**: View complete user information in a modal
- **Search Users**: Real-time search functionality
- **User Management**: Full CRUD operations for computer lab users
- **Last Login Tracking**: Automatically tracks when users sign in to use computers (using system local time)

## How It Works

### 1. Form Submission
- Forms use `method="POST"` and `action="{% url 'view_name' %}"`
- CSRF tokens are automatically included for security
- Data is processed directly in Django views

### 2. Database Operations
- **Create**: `ComputerUser.objects.create()` in `add_user` view
- **Read**: `ComputerUser.objects.all()` in `computer_users` view
- **Update**: `user.save()` in `edit_user` view
- **View Details**: `get_object_or_404(ComputerUser, id=user_id)` in `view_user_details`

### 3. URL Patterns
```python
path('computer_users/add/', views.add_user, name='add_user'),
path('computer_users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
path('computer_users/view/<int:user_id>/', views.view_user_details, name='view_user_details'),
```

### 4. Views
- `add_user()`: Handles POST requests to create new users
- `edit_user(user_id)`: Handles POST requests to update existing users
- `view_user_details(user_id)`: Handles GET requests to retrieve user details
- `computer_users()`: Displays all users with pagination

## Key Benefits

1. **No JavaScript API Calls**: All data operations happen through Django forms
2. **Built-in Security**: CSRF protection, form validation, and SQL injection prevention
3. **Django Messages**: User feedback through Django's message framework
4. **Database Integrity**: Direct model operations ensure data consistency
5. **SEO Friendly**: Traditional form submissions work without JavaScript

## Usage

1. **Add a User**: Click "Add New User" button, fill the form, and submit
2. **Edit a User**: Click the edit button (pencil icon) next to any user
3. **View User Details**: Click the eye icon to view complete user information
4. **Search Users**: Use the search box to filter users in real-time
5. **Track Last Login**: Last login time is automatically updated when users sign in via the kiosk (using system local time)

## Database Schema

The `ComputerUser` model includes:
- Basic information (name, email, contact details)
- Academic details (student ID, course)
- Access control (access level, status)
- System information (computer station, last login timestamps)

## Running the Project

1. Install dependencies: `pip install django`
2. Run migrations: `python manage.py migrate`
3. Start server: `python manage.py runserver`
4. Visit: `http://localhost:8000/computer_users/`

## File Structure

- `mainpage/views.py`: Contains all view functions for handling form submissions
- `mainpage/urls.py`: URL routing for form actions
- `mainpage/models.py`: Database model definition
- `mainpage/templates/computer_users.html`: HTML template with forms
- `mainpage/static/`: CSS and JavaScript files

This approach provides a robust, secure, and maintainable way to handle database operations without the complexity of API endpoints. 