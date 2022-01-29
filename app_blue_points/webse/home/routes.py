import os
import secrets
import json
from datetime import timedelta, datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, Blueprint
from webse import app, db, bcrypt
from webse.models import User, Moduls, Announcement, Chat, Emissions
from flask_login import login_user, current_user, logout_user, login_required

home= Blueprint('home', __name__)


###########################
####   Block 0. Home   ####
###########################
@home.route('/home')
@home.route('/')
def home_main():
    page = request.args.get('page', 1, type=int)
    announcements = Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=page, per_page=1)
    return render_template('home.html', announcements=announcements, title='Home')


###############################
####   Block 8. Teachers   ####
###############################
@home.route('/teachers')
def teachers():
	return render_template('teachers.html', title='Teachers')