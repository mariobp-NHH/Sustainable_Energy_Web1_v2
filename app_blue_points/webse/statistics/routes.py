import os
import secrets
import json
from datetime import timedelta, datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, Blueprint
from webse import app, db, bcrypt
from webse.models import User, Moduls, Announcement, Chat, Emissions
from flask_login import login_user, current_user, logout_user, login_required

statistics = Blueprint('statistics', __name__)

##################################
####   Block 11. Statistics   ####
##################################

@statistics.route('/statistics', methods=['GET', 'POST'])
@login_required
def statistics_main():
    entries = Moduls.query.filter_by(author=current_user).filter(Moduls.title_mo.is_('---')).order_by(Moduls.date_exercise.desc()).all()
    return render_template('statistics/statistics.html',entries=entries, correct=0, incorrect=0)

@statistics.route('/statistics/se_ch1', methods=['GET', 'POST'])
@login_required
def statistics_se_ch1():
    entries = Moduls.query.filter_by(author=current_user). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
        filter(Moduls.question_option.is_(50)). \
        order_by(Moduls.question_num.asc()).all()

    incorrect = Moduls.query.filter_by(author=current_user). \
        filter(Moduls.question_result.is_(0)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
        filter(Moduls.question_option.is_(50)). \
        order_by(Moduls.question_num.asc()).count()

    correct = Moduls.query.filter_by(author=current_user). \
        filter(Moduls.question_result.is_(1)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
        filter(Moduls.question_option.is_(50)). \
        order_by(Moduls.question_num.asc()).count()

    flash('Your answer has been submitted!', 'success')
    return render_template('statistics/statistics_se_ch1.html', entries=entries, correct=correct, incorrect=incorrect)

@statistics.route('/statistics/se_ch2', methods=['GET', 'POST'])
@login_required
def statistics_se_ch2():
    entries = Moduls.query.filter_by(author=current_user). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(50)). \
        order_by(Moduls.question_num.asc()).all()

    incorrect = Moduls.query.filter_by(author=current_user). \
        filter(Moduls.question_result.is_(0)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(50)). \
        order_by(Moduls.question_num.asc()).count()

    correct = Moduls.query.filter_by(author=current_user). \
        filter(Moduls.question_result.is_(1)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(50)). \
        order_by(Moduls.question_num.asc()).count()
    flash('Your answer has been submitted!', 'success')
    return render_template('statistics/statistics_se_ch2.html', entries=entries, correct=correct, incorrect=incorrect)

@statistics.route('/statistics/se_ch3', methods=['GET', 'POST'])
@login_required
def statistics_se_ch3():
    entries = Moduls.query.filter_by(author=current_user). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
        filter(Moduls.question_option.is_(50)). \
        order_by(Moduls.question_num.asc()).all()

    incorrect = Moduls.query.filter_by(author=current_user). \
        filter(Moduls.question_result.is_(0)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
        filter(Moduls.question_option.is_(50)). \
        order_by(Moduls.question_num.asc()).count()

    correct = Moduls.query.filter_by(author=current_user). \
        filter(Moduls.question_result.is_(1)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
        filter(Moduls.question_option.is_(50)). \
        order_by(Moduls.question_num.asc()).count()
    flash('Your answer has been submitted!', 'success')
    return render_template('statistics/statistics_se_ch3.html', entries=entries, correct=correct, incorrect=incorrect)