# routes.py
from app import myapp_obj, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .forms import LoginForm, RegistrationForm, ProfileForm, EditProfileForm
from .models import User, Role

@myapp_obj.route('/')
@myapp_obj.route('/home')
def home():
    # Redirect logged-in users to the dashboard page
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@myapp_obj.route('/dashboard')
@login_required
def dashboard():
    # Pass the first name and role of the current user to the template
    name = current_user.first_name
    role = current_user.role
    return render_template('dashboard.html', first_name=name, user_role=role)

@myapp_obj.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to home page if user is already logged in
    if current_user.is_authenticated:
        name = current_user.first_name
        role = current_user.role
        return render_template('dashboard.html', first_name=name, user_role=role)
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # Log in the user
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))  # Redirect to the dashboard or the page they were trying to access
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@myapp_obj.route('/logout')
def logout():
    # Log out the user if they are authenticated
    if current_user.is_authenticated:
        logout_user()
        flash('Logged out.', 'success') # Flash message
    # Redirect to the home page
    return redirect(url_for('home'))

@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Create the user object and set its attributes
            new_user = User(username=form.username.data, 
                            role=form.role.data, 
                            first_name=form.first_name.data, 
                            last_name=form.last_name.data,
                            created_at=datetime.utcnow())
            
            # Check if the role is librarian and set the permission
            if form.role.data == 'librarian':
                librarian_role = Role.query.filter_by(name='librarian').first()
                if librarian_role:
                    librarian_role.can_view_users = True
                else:
                    librarian_role.can_view_users = False

            
            # Hash the password with salt (SHA256)
            new_user.set_password(form.password.data)
            # Add the user to the database session and commit the transaction
            db.session.add(new_user)
            db.session.commit()
        
            # Redirect to login page upon successful registration
            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            # Handle the case when the username already exists
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', form=form, error=error)

    return render_template('register.html', form=form)


@myapp_obj.route('/profile')
@login_required
def profile():
    # Create a profile form and pre-fill it with the current user's information
    form = ProfileForm()
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.username.data = current_user.username
    form.role.data = current_user.role
    form.created_at.data = current_user.created_at.strftime("%m-%d-%Y")  

    # Render the profile template with the readonly profile form
    return render_template('profile.html', form=form)

@myapp_obj.route('/view_users')
@login_required
def view_users():
    if current_user.role != 'librarian':
        flash('You do not have permission to view users.', 'danger')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()  # Get all users
    return render_template('view_users.html', users=users)

@myapp_obj.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)  # Get the user by ID or return 404 if not found
    
    # Check if the current user has permission to edit this user's information
    if current_user.role != 'librarian' and current_user.id != user.id:
        flash('You do not have permission to edit this user.', 'danger')
        return redirect(url_for('view_users'))
    
    form = EditProfileForm(obj=user)  # Pass the user object to pre-fill the form
    
    if form.validate_on_submit():
        # Update user information
        user.update_info(form.first_name.data,
                         form.last_name.data,
                         form.username.data,
                         form.role.data)
        # Commit changes to the database
        db.session.commit()
        flash('User information updated successfully.', 'success')
        return redirect(url_for('view_users'))
    form.created_at.data = current_user.created_at.strftime("%m-%d-%Y")
    
    return render_template('edit_user.html', form=form)


@myapp_obj.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)  # Get the user by ID or return 404 if not found
    
    # Check if the current user has permission to delete this user
    if current_user.role != 'librarian':
        flash('You do not have permission to delete users.', 'danger')
        return redirect(url_for('view_users'))
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('view_users'))