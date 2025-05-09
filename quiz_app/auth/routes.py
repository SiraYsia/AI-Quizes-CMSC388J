from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from quiz_app import bcrypt, mongo
from quiz_app.models import User
from quiz_app.auth.forms import RegistrationForm, LoginForm
from quiz_app.user.forms import ResetPasswordForm
from . import auth
from bson.objectid import ObjectId

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user_data = {
            'username': form.username.data,
            'email': form.email.data,
            'password': hashed_password
        }
        
        mongo.db.users.insert_one(user_data)
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user_data = mongo.db.users.find_one({'email': form.email.data})
        
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user = User(user_data)
            login_user(user, remember=form.remember.data)
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            
            mongo.db.users.update_one(
                {'_id': ObjectId(current_user.id)},
                {'$set': {'password': hashed_password}}
            )
            
            flash('Your password has been updated!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('Current password is incorrect.', 'danger')
    
    return render_template('user/reset_password.html', title='Reset Password', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))