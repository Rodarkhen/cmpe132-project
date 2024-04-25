# routes.py
from app import myapp_obj, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .forms import LoginForm, RegistrationForm
from .models import User

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
            # Hash the password
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
