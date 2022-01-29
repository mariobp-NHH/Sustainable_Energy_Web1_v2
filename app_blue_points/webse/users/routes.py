import os
import secrets
import json
from datetime import timedelta, datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, Blueprint
from webse import app, db, bcrypt
from webse.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from webse.models import User, Moduls, Announcement, Chat, Emissions
from flask_login import login_user, current_user, logout_user, login_required
from webse.users.utils import save_picture

users = Blueprint('users', __name__)

######################################
####   Block 1. User Information   ###
######################################
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, course=form.course.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home_main'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('user/login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home.home_main'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user/account.html', title='Account',
                           image_file=image_file, form=form)

@users.route("/chat/user/<string:username>")
def user_chats(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    chats = Chat.query.filter_by(author=user)\
        .order_by(Chat.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('chat/user_chats.html', chats=chats, user=user)

@users.route("/announcement/user/<string:username>")
def user_announcements(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    announcements = Announcement.query.filter_by(author=user)\
        .order_by(Announcement.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('announcement/user_announcements.html', announcements=announcements, user=user)
