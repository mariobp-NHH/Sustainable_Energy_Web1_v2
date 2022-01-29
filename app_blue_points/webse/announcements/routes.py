import os
import secrets
import json
from datetime import timedelta, datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, Blueprint
from webse import app, db, bcrypt
from webse.announcements.forms import AnnouncementForm
from webse.models import User, Moduls, Announcement, Chat, Emissions
from flask_login import login_user, current_user, logout_user, login_required

announcements = Blueprint('announcements', __name__)

##################################
####   Block 2. Announcement   ###
###################################

@announcements.route("/announcement/new", methods=['GET', 'POST'])
@login_required
def new_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(announcement)
        db.session.commit()
        flash('Your announcement has been created!', 'success')
        return redirect(url_for('home.home_main'))
    return render_template('announcement/create_announcement.html', title='New Announcement',
                           form=form, legend='New Announcement')

@announcements.route("/announcement/<int:announcement_id>")
def announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    return render_template('announcement/announcement.html', title=announcement.title, announcement=announcement)



@announcements.route("/announcement/<int:announcement_id>/update", methods=['GET', 'POST'])
@login_required
def update_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    if announcement.author != current_user:
        abort(403)
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        db.session.commit()
        flash('Your announcement has been updated!', 'success')
        return redirect(url_for('announcements.announcement', announcement_id=announcement.id))
    elif request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
    return render_template('announcement/create_announcement.html', title='Update Announcement',
                           form=form, legend='Update Announcement')


@announcements.route("/announcement/<int:announcement_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(int(announcement_id))
    if announcement.author != current_user:
        abort(403)
    db.session.delete(announcement)
    db.session.commit()
    flash('Your announcement has been deleted!', 'success')
    return redirect(url_for('home.home_main'))
