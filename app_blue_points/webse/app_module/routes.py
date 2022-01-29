import os
import secrets
import json
from datetime import timedelta, datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, Blueprint
from webse import app, db, bcrypt
from webse.app_module.forms import ChatFormUpdate
from webse.app_module.forms import ModulsForm_m1_ch1_q1, ModulsForm_m1_ch1_q2, ModulsForm_m1_ch1_q3
from webse.app_module.forms import ModulsForm_m1_ch2_q1, ModulsForm_m1_ch2_q2, ModulsForm_m1_ch2_q3, ModulsForm_m1_ch2_q4, ModulsForm_m1_ch2_q5
from webse.models import User, Moduls, Announcement, Chat, Emissions
from flask_login import login_user, current_user, logout_user, login_required

app_module = Blueprint('app_module', __name__)

#################################
####   Block 9. App Module   ####
#################################
# App web
@app_module.route('/app_web')
@login_required
def app_web():
	return render_template('app web/app_web.html', title='App Web')

# App Module, Chapter 1.
@app_module.route('/app_web/ch1', methods=['GET', 'POST'])
@login_required
def app_web_ch1():
    form_m1_ch1_q1 = ModulsForm_m1_ch1_q1()
    form_m1_ch1_q2 = ModulsForm_m1_ch1_q2()
    form_m1_ch1_q3 = ModulsForm_m1_ch1_q3()

    if form_m1_ch1_q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user).\
            filter(Moduls.title_mo.is_('App Development')).\
            filter(Moduls.title_ch.is_('Ch1. Introduction')).\
            filter(Moduls.question_num.is_(1)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m1_ch1_q1.type.data, author=current_user)
        if moduls.question_str == 'Python':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'App Development'
        moduls.title_ch = 'Ch1. Introduction'
        moduls.question_num = 1
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('app_web_ch1'))

    if form_m1_ch1_q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch1. Introduction')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m1_ch1_q2.type.data, author=current_user)
        if moduls.question_str == 'GitHub':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'App Development'
        moduls.title_ch = 'Ch1. Introduction'
        moduls.question_num = 2
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('app_web_ch1'))

    if form_m1_ch1_q3.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch1. Introduction')). \
            filter(Moduls.question_num.is_(3)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m1_ch1_q3.type.data, author=current_user)
        if moduls.question_str == 'Easy':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'App Development'
        moduls.title_ch = 'Ch1. Introduction'
        moduls.question_num = 3
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('app_web_ch1'))

    return render_template('app web/app_web_ch1.html', title='App Web - Ch1',
                           form_m1_ch1_q1=form_m1_ch1_q1, form_m1_ch1_q2=form_m1_ch1_q2,
                           form_m1_ch1_q3=form_m1_ch1_q3)

# App Module, Chapter 2.
@app_module.route('/app_web/ch2', methods=['GET', 'POST'])
@login_required
def app_web_ch2():
    form_m1_ch2_q1 = ModulsForm_m1_ch2_q1()
    form_m1_ch2_q2 = ModulsForm_m1_ch2_q2()
    form_m1_ch2_q3 = ModulsForm_m1_ch2_q3()
    form_m1_ch2_q4 = ModulsForm_m1_ch2_q4()
    form_m1_ch2_q5 = ModulsForm_m1_ch2_q5()

    if form_m1_ch2_q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(1)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m1_ch2_q1.question_str.data, author=current_user)
        if moduls.question_str == 'yes':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'App Development'
        moduls.title_ch = 'Ch2. Installation'
        moduls.question_num = 1
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('app_web_ch2'))

    if form_m1_ch2_q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m1_ch2_q2.type.data, author=current_user)
        if moduls.question_str == 'wind':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'App Development'
        moduls.title_ch = 'Ch2. Installation'
        moduls.question_num = 2
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('app_web_ch2'))

    if form_m1_ch2_q3.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(3)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m1_ch2_q3.type.data, author=current_user)
        if moduls.question_str == 'income':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'App Development'
        moduls.title_ch = 'Ch2. Installation'
        moduls.question_num = 3
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('app_web_ch2'))

    if form_m1_ch2_q4.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(4)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m1_ch2_q4.type.data, author=current_user)
        if moduls.question_str == 'school':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'App Development'
        moduls.title_ch = 'Ch2. Installation'
        moduls.question_num = 4
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('app_web_ch2'))

    if form_m1_ch2_q5.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(5)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m1_ch2_q5.type.data, author=current_user)
        if moduls.question_str == 'Hydrogen':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'App Development'
        moduls.title_ch = 'Ch2. Installation'
        moduls.question_num = 5
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('app_web_ch2'))

    return render_template('app web/app_web_ch2.html', title='App Web - Ch2',
                           form_m1_ch2_q1=form_m1_ch2_q1, form_m1_ch2_q2=form_m1_ch2_q2, form_m1_ch2_q3 = form_m1_ch2_q3,
                           form_m1_ch2_q4=form_m1_ch2_q4, form_m1_ch2_q5=form_m1_ch2_q5)
