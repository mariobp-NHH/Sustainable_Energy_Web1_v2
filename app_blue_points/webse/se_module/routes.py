from flask import render_template, url_for, flash, redirect, request, abort, jsonify, Blueprint
from webse import db
from webse.se_module.forms import ChatFormUpdate
from webse.se_module.forms import ModulsForm_m2_ch1_e1, ModulsForm_m2_ch1_e2, ModulsForm_m2_ch1_q1, ModulsForm_m2_ch1_q2
from webse.se_module.forms import ModulsForm_m2_ch2_e1, ModulsForm_m2_ch2_e2, ModulsForm_m2_ch2_e3, ModulsForm_m2_ch2_q1, ModulsForm_m2_ch2_q2
from webse.se_module.forms import ModulsForm_m2_ch2_q3, ModulsForm_m2_ch2_q4, ModulsForm_m2_ch2_q5, ModulsForm_m2_ch2_q6, ModulsForm_m2_ch2_q7, ModulsForm_m2_ch2_q8
from webse.se_module.forms import ModulsForm_m2_ch3_e1, ModulsForm_m2_ch3_e2, ModulsForm_m2_ch3_q1, ModulsForm_m2_ch3_q2
from webse.se_module.forms import ModulsForm_m2_ch3_q3, ModulsForm_m2_ch3_q4, ModulsForm_m2_ch3_q5, ModulsForm_m2_ch3_q6, ModulsForm_m2_ch3_q7, ModulsForm_m2_ch3_q8, ModulsForm_m2_ch3_q9
from webse.models import Moduls, Chat
from flask_login import login_user, current_user, logout_user, login_required

se_module = Blueprint('se_module', __name__)


@se_module.route('/sustainable_energy_web')
@login_required
def sustainable_energy_web():
	return render_template('se web/sustainable_energy_web.html', title='SE Web')

##########################################
## Sustainable Energy Module, Chapter 1 ##
##########################################
@se_module.route('/sustainable_energy_web/ch1', methods=['GET', 'POST'])
@login_required
def se_web_ch1():
    form_m2_ch1_q1 = ModulsForm_m2_ch1_q1()
    form_m2_ch1_q2 = ModulsForm_m2_ch1_q2()

    if form_m2_ch1_q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
            filter(Moduls.question_num.is_(1)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch1_q1.type.data, author=current_user)
        if moduls.question_str == 'Should also consider social aspects':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Chapter 1. Frame'
        moduls.question_num = 1
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch1'))

    if form_m2_ch1_q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch1_q2.type.data, author=current_user)
        if moduls.question_str == 'Sustainability and economy are a subsystem of the ecosystem':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Chapter 1. Frame'
        moduls.question_num = 2
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch1'))
    return render_template('se web/ch1/se_web_ch1.html', title='SE Web - Ch1',
                           form_m2_ch1_q1=form_m2_ch1_q1,
                           form_m2_ch1_q2=form_m2_ch1_q2)

#SE, Ch1, Exercise 1.
@se_module.route('/sustainable_energy_web/ch1/ex1', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex1():
    return render_template('se web/ch1/se_web_ch1_ex1.html', title='SE Web - Ch1 - Ex1')

@se_module.route('/sustainable_energy_web/ch1/ex1/questionnaire', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex1_questionnaire():
    form_m2_ch1_e1 = ModulsForm_m2_ch1_e1()

    if form_m2_ch1_e1.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
            filter(Moduls.question_num.is_(11)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch1_e1.type.data, author=current_user)
        if moduls.question_str == 'Should include only environmental pollution, carbon emissions':
            moduls.question_option = 1
        elif moduls.question_str == 'Should include only poverty alleviation, gender equality':
            moduls.question_option = 2
        else:
            moduls.question_option = 3
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Chapter 1. Frame'
        moduls.question_num = 11
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch1_ex1_questionnaire'))
    return render_template('se web/ch1/se_web_ch1_ex1_questionnaire.html', title='SE Web - Ch1 - Ex1',
                           form_m2_ch1_e1=form_m2_ch1_e1)

@se_module.route('/sustainable_energy_web/ch1/ex1/questionnaire/refresh', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex1_questionnaire_refresh():
    form_m2_ch1_e1 = ModulsForm_m2_ch1_e1()
    option_1 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
        filter(Moduls.question_option.is_(1)). \
        order_by(Moduls.question_num.asc()).count()

    option_2 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
        filter(Moduls.question_option.is_(2)). \
        order_by(Moduls.question_num.asc()).count()

    option_3 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
        filter(Moduls.question_option.is_(3)). \
        order_by(Moduls.question_num.asc()).count()
    return render_template('se web/ch1/se_web_ch1_ex1_questionnaire.html', title='SE Web - Ch1 - Ex1',
                           option_1=option_1,option_2=option_2,option_3=option_3,
                           form_m2_ch1_e1=form_m2_ch1_e1)


@se_module.route('/sustainable_energy_web/ch1/ex1/chat', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex1_chat():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user,
                    chat_module='SE_ch1_ex1',
                    chat_group='Exercise 1')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('se_module.se_web_ch1_ex1_chat_query'))
    return render_template('se web/ch1/se_web_ch1_ex1_chat_create.html', title='SE Web - Ch1 - Ex1',
                           form= form, legend='Sustainable Energy, Chapter 1, Exercise 1')

@se_module.route('/sustainable_energy_web/ch1/ex1/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex1_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch1_ex1')).order_by(Chat.date_posted.desc()).paginate(page=page,
                                                                                                            per_page=4)
    return render_template('se web/ch1/se_web_ch1_ex1_chat_query.html', title='SE Web - Ch1 - Ex1',
                           chats=chats, legend='Sustainable Energy, Chapter 1, Exercise 1')

#SE, Ch1, Exercise 2.
@se_module.route('/sustainable_energy_web/ch1/ex2', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex2():
    return render_template('se web/ch1/se_web_ch1_ex2.html', title='SE Web - Ch1 - ex2')

@se_module.route('/sustainable_energy_web/ch1/ex2/questionnaire', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex2_questionnaire():
    form_m2_ch1_e2 = ModulsForm_m2_ch1_e2()

    if form_m2_ch1_e2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
            filter(Moduls.question_num.is_(22)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch1_e2.type.data, author=current_user)
        if moduls.question_str == 'Green Economy is more related to welfare and environmental economics':
            moduls.question_option = 1
        elif moduls.question_str == 'Green Economy is more related to ecological economics':
            moduls.question_option = 2
        else:
            moduls.question_option = 3
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Chapter 1. Frame'
        moduls.question_num = 22
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch1_ex2_questionnaire'))
    return render_template('se web/ch1/se_web_ch1_ex2_questionnaire.html', title='SE Web - Ch1 - ex2',
                           form_m2_ch1_e2=form_m2_ch1_e2)

@se_module.route('/sustainable_energy_web/ch1/ex2/questionnaire/refresh', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex2_questionnaire_refresh():
    form_m2_ch1_e2 = ModulsForm_m2_ch1_e2()
    option_1 = Moduls.query.filter(Moduls.question_num.is_(22)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
        filter(Moduls.question_option.is_(1)). \
        order_by(Moduls.question_num.asc()).count()

    option_2 = Moduls.query.filter(Moduls.question_num.is_(22)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
        filter(Moduls.question_option.is_(2)). \
        order_by(Moduls.question_num.asc()).count()

    option_3 = Moduls.query.filter(Moduls.question_num.is_(22)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 1. Frame')). \
        filter(Moduls.question_option.is_(3)). \
        order_by(Moduls.question_num.asc()).count()

    return render_template('se web/ch1/se_web_ch1_ex2_questionnaire.html', title='SE Web - Ch1 - Ex2',
                           option_1=option_1,option_2=option_2,option_3=option_3,
                           form_m2_ch1_e2=form_m2_ch1_e2)

@se_module.route('/sustainable_energy_web/ch1/ex2/chat', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex2_chat():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user,
                    chat_module='SE_ch1_ex2',
                    chat_group='Exercise 2')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('se_module.se_web_ch1_ex2_chat_query'))
    return render_template('se web/ch1/se_web_ch1_ex2_chat_create.html', title='SE Web - Ch1 - Ex2',
                           form= form, legend='Sustainable Energy, Chapter 1, Exercise 2')

@se_module.route('/sustainable_energy_web/ch1/ex2/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex2_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch1_ex2')).order_by(Chat.date_posted.desc()).paginate(page=page,
                                                                                                            per_page=4)
    return render_template('se web/ch1/se_web_ch1_ex2_chat_query.html', title='SE Web - Ch1 - ex2',
                           chats=chats, legend='Sustainable Energy, Chapter 1, Exercise 2')


##########################################
## Sustainable Energy Module, Chapter 2 ##
##########################################
@se_module.route('/sustainable_energy_web/ch2', methods=['GET', 'POST'])
@login_required
def se_web_ch2():
    form_m2_ch2_q1 = ModulsForm_m2_ch2_q1()
    form_m2_ch2_q2 = ModulsForm_m2_ch2_q2()
    form_m2_ch2_q3 = ModulsForm_m2_ch2_q3()
    form_m2_ch2_q4 = ModulsForm_m2_ch2_q4()
    form_m2_ch2_q5 = ModulsForm_m2_ch2_q5()
    form_m2_ch2_q6 = ModulsForm_m2_ch2_q6()
    form_m2_ch2_q7 = ModulsForm_m2_ch2_q7()
    form_m2_ch2_q8 = ModulsForm_m2_ch2_q8()

    if form_m2_ch2_q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user).\
            filter(Moduls.title_mo.is_('Sustainable Energy')).\
            filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')).\
            filter(Moduls.question_num.is_(1)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_q1.type.data, author=current_user)
        if moduls.question_str == 'Biologically productive area it takes to satisfy the demands of people':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Ecological Footprint and Biocapacity'
        moduls.question_num = 1
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2'))

    if form_m2_ch2_q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_q2.type.data, author=current_user)
        if moduls.question_str == 'Land and sea area available to provide the resources a population consumes and to absorb its wastes':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Ecological Footprint and Biocapacity'
        moduls.question_num = 2
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2'))

    if form_m2_ch2_q3.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(3)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_q3.type.data, author=current_user)
        if moduls.question_str == 'Both':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Ecological Footprint and Biocapacity'
        moduls.question_num = 3
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2'))

    if form_m2_ch2_q4.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(4)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_q4.type.data, author=current_user)
        if moduls.question_str == 'Both':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Ecological Footprint and Biocapacity'
        moduls.question_num = 4
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2'))

    if form_m2_ch2_q5.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(5)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_q5.type.data, author=current_user)
        if moduls.question_str == 'Reflect the relative productivity of a given land use type':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Ecological Footprint and Biocapacity'
        moduls.question_num = 5
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2'))

    if form_m2_ch2_q6.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(6)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_q6.type.data, author=current_user)
        if moduls.question_str == 'Very suitable, suitable, moderately suitable, marginally suitable, and not suitable':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Ecological Footprint and Biocapacity'
        moduls.question_num = 6
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2'))

    if form_m2_ch2_q7.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(7)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_q7.type.data, author=current_user)
        if moduls.question_str == 'In the 70s':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Ecological Footprint and Biocapacity'
        moduls.question_num = 7
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2'))

    if form_m2_ch2_q8.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(8)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_q8.type.data, author=current_user)
        if moduls.question_str == 'It represents the 60%':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Ecological Footprint and Biocapacity'
        moduls.question_num = 8
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2'))
    return render_template('se web/ch2/se_web_ch2.html', title='SE Web - Ch2',
                           form_m2_ch2_q1=form_m2_ch2_q1, form_m2_ch2_q2=form_m2_ch2_q2,
                           form_m2_ch2_q3=form_m2_ch2_q3, form_m2_ch2_q4=form_m2_ch2_q4,
                           form_m2_ch2_q5=form_m2_ch2_q5, form_m2_ch2_q6=form_m2_ch2_q6,
                           form_m2_ch2_q7=form_m2_ch2_q7, form_m2_ch2_q8=form_m2_ch2_q8)

#SE, Ch2, Exercise 1.
@se_module.route('/sustainable_energy_web/ch2/ex1', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex1():
    return render_template('se web/ch2/se_web_ch2_ex1.html', title='SE Web - ch2 - Ex1')

@se_module.route('/sustainable_energy_web/ch2/ex1/questionnaire', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex1_questionnaire():
    form_m2_ch2_e1 = ModulsForm_m2_ch2_e1()

    if form_m2_ch2_e1.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(11)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_e1.type.data, author=current_user)
        if moduls.question_str == 'The ecological footprint should be charged to Norway':
            moduls.question_option = 1
        elif moduls.question_str == 'The ecological footprint should be charged to Spain':
            moduls.question_option = 2
        else:
            moduls.question_option = 3
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Chapter 2. Ecological Footprint and Biocapacity'
        moduls.question_num = 11
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2_ex1_questionnaire'))
    return render_template('se web/ch2/se_web_ch2_ex1_questionnaire.html', title='SE Web - ch2 - Ex1',
                           form_m2_ch2_e1=form_m2_ch2_e1)

@se_module.route('/sustainable_energy_web/ch2/ex1/questionnaire/refresh', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex1_questionnaire_refresh():
    form_m2_ch2_e1 = ModulsForm_m2_ch2_e1()
    option_1 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(1)). \
        order_by(Moduls.question_num.asc()).count()

    option_2 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(2)). \
        order_by(Moduls.question_num.asc()).count()

    option_3 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(3)). \
        order_by(Moduls.question_num.asc()).count()
    return render_template('se web/ch2/se_web_ch2_ex1_questionnaire.html', title='SE Web - ch2 - Ex1',
                           option_1=option_1,option_2=option_2,option_3=option_3,
                           form_m2_ch2_e1=form_m2_ch2_e1)

@se_module.route('/sustainable_energy_web/ch2/ex1/chat', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex1_chat():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user,
                    chat_module='SE_ch2_ex1',
                    chat_group='Exercise 1')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('se_module.se_web_ch2_ex1_chat_query'))
    return render_template('se web/ch2/se_web_ch2_ex1_chat_create.html', title='SE Web - ch2 - Ex1',
                           form= form, legend='Sustainable Energy, Chapter 2, Exercise 1')

@se_module.route('/sustainable_energy_web/ch2/ex1/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex1_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch2_ex1')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('se web/ch2/se_web_ch2_ex1_chat_query.html', title='SE Web - ch2 - Ex1',
                           chats=chats, legend='Sustainable Energy, Chapter 2, Exercise 1')

#SE, Ch2, Exercise 2.
@se_module.route('/sustainable_energy_web/ch2/ex2', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex2():
    return render_template('se web/ch2/se_web_ch2_ex2.html', title='SE Web - ch2 - ex2')

@se_module.route('/sustainable_energy_web/ch2/ex2/questionnaire', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex2_questionnaire():
    form_m2_ch2_e2 = ModulsForm_m2_ch2_e2()

    if form_m2_ch2_e2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(11)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_e2.type.data, author=current_user)
        if moduls.question_str == 'Land to capture carbon emissions':
            moduls.question_option = 1
        elif moduls.question_str == 'Cropland, grazing land, fishing grounds, forest products land':
            moduls.question_option = 2
        else:
            moduls.question_option = 3
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Chapter 2. Ecological Footprint and Biocapacity'
        moduls.question_num = 11
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2_ex2_questionnaire'))
    return render_template('se web/ch2/se_web_ch2_ex2_questionnaire.html', title='SE Web - ch2 - ex2',
                           form_m2_ch2_e2=form_m2_ch2_e2)

@se_module.route('/sustainable_energy_web/ch2/ex2/questionnaire/refresh', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex2_questionnaire_refresh():
    form_m2_ch2_e2 = ModulsForm_m2_ch2_e2()
    option_1 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(1)). \
        order_by(Moduls.question_num.asc()).count()

    option_2 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(2)). \
        order_by(Moduls.question_num.asc()).count()

    option_3 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(3)). \
        order_by(Moduls.question_num.asc()).count()
    return render_template('se web/ch2/se_web_ch2_ex2_questionnaire.html', title='SE Web - ch2 - ex2',
                           option_1=option_1,option_2=option_2,option_3=option_3,
                           form_m2_ch2_e2=form_m2_ch2_e2)

@se_module.route('/sustainable_energy_web/ch2/ex2/chat', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex2_chat():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user,
                    chat_module='SE_ch2_ex2',
                    chat_group='Exercise 2')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('se_module.se_web_ch2_ex2_chat_query'))
    return render_template('se web/ch2/se_web_ch2_ex2_chat_create.html', title='SE Web - ch2 - ex2',
                           form= form, legend='Sustainable Energy, Chapter 2, Exercise 2')

@se_module.route('/sustainable_energy_web/ch2/ex2/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex2_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch2_ex2')).order_by(Chat.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template('se web/ch2/se_web_ch2_ex2_chat_query.html', title='SE Web - ch2 - ex2',
                           chats=chats, legend='Sustainable Energy, Chapter 2, Exercise 2')

#SE, Ch2, Exercise 3.
@se_module.route('/sustainable_energy_web/ch2/ex3', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex3():
    return render_template('se web/ch2/se_web_ch2_ex3.html', title='SE Web - ch2 - ex3')

@se_module.route('/sustainable_energy_web/ch2/ex3/questionnaire', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex3_questionnaire():
    form_m2_ch2_e3 = ModulsForm_m2_ch2_e3()

    if form_m2_ch2_e3.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
            filter(Moduls.question_num.is_(11)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch2_e3.type.data, author=current_user)
        if moduls.question_str == 'Land to capture carbon emissions':
            moduls.question_option = 1
        elif moduls.question_str == 'Cropland':
            moduls.question_option = 2
        else:
            moduls.question_option = 3
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Chapter 2. Ecological Footprint and Biocapacity'
        moduls.question_num = 11
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch2_ex3_questionnaire'))

    return render_template('se web/ch2/se_web_ch2_ex3_questionnaire.html', title='SE Web - ch2 - ex3',
                           form_m2_ch2_e3=form_m2_ch2_e3)

@se_module.route('/sustainable_energy_web/ch2/ex3/questionnaire/refresh', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex3_questionnaire_refresh():
    form_m2_ch2_e3 = ModulsForm_m2_ch2_e3()
    option_1 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(1)). \
        order_by(Moduls.question_num.asc()).count()

    option_2 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(2)). \
        order_by(Moduls.question_num.asc()).count()

    option_3 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Chapter 2. Ecological Footprint and Biocapacity')). \
        filter(Moduls.question_option.is_(3)). \
        order_by(Moduls.question_num.asc()).count()
    return render_template('se web/ch2/se_web_ch2_ex3_questionnaire.html', title='SE Web - ch2 - ex3',
                           option_1=option_1,option_2=option_2,option_3=option_3,
                           form_m2_ch2_e3=form_m2_ch2_e3)

@se_module.route('/sustainable_energy_web/ch2/ex3/chat', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex3_chat():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user,
                    chat_module='SE_ch2_ex3',
                    chat_group='Exercise 3')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('se_module.se_web_ch2_ex3_chat_query'))
    return render_template('se web/ch2/se_web_ch2_ex3_chat_create.html', title='SE Web - ch2 - ex3',
                           form= form, legend='Sustainable Energy, Chapter 2, Exercise 3')

@se_module.route('/sustainable_energy_web/ch2/ex3/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex3_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch2_ex3')).order_by(Chat.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template('se web/ch2/se_web_ch2_ex3_chat_query.html', title='SE Web - ch2 - ex3',
                           chats=chats, legend='Sustainable Energy, Chapter 2, Exercise 3')

##########################################
## Sustainable Energy Module, Chapter 3 ##
##########################################
@se_module.route('/sustainable_energy_web/ch3', methods=['GET', 'POST'])
@login_required
def se_web_ch3():
    form_m2_ch3_q1 = ModulsForm_m2_ch3_q1()
    form_m2_ch3_q2 = ModulsForm_m2_ch3_q2()
    form_m2_ch3_q3 = ModulsForm_m2_ch3_q3()
    form_m2_ch3_q4 = ModulsForm_m2_ch3_q4()
    form_m2_ch3_q5 = ModulsForm_m2_ch3_q5()
    form_m2_ch3_q6 = ModulsForm_m2_ch3_q6()
    form_m2_ch3_q7 = ModulsForm_m2_ch3_q7()
    form_m2_ch3_q8 = ModulsForm_m2_ch3_q8()
    form_m2_ch3_q9 = ModulsForm_m2_ch3_q9()

    if form_m2_ch3_q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user).\
            filter(Moduls.title_mo.is_('Sustainable Energy')).\
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')).\
            filter(Moduls.question_num.is_(1)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q1.type.data, author=current_user)
        if moduls.question_str == 'The debate about the starting date of the Antrophocene is still open':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 1
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3'))

    if form_m2_ch3_q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q2.type.data, author=current_user)
        if moduls.question_str == 'Increase in arid areas':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 2
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3'))


    if form_m2_ch3_q3.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(3)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q3.type.data, author=current_user)
        if moduls.question_str == 'Those elements do not interact with humans, and determine the relations of power and culture':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 3
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3'))

    if form_m2_ch3_q4.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(4)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q2.type.data, author=current_user)
        if moduls.question_str == 'Biodiversity loss, climate crisis, and nitrogen cycle':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 4
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3'))

    if form_m2_ch3_q5.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(5)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q5.type.data, author=current_user)
        if moduls.question_str == 'They are two interdependent imbalances that reinforce each other':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 5
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3'))

    if form_m2_ch3_q6.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(6)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q6.type.data, author=current_user)
        if moduls.question_str == 'The cost of carbon in 2030 will be $75 per tonne of carbon dioxide in 2017 US dollars':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 6
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3'))

    if form_m2_ch3_q7.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(7)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q7.type.data, author=current_user)
        if moduls.question_str == 'Multiplying the HDI by the arithmetic mean of the social cost of carbon emissions and the ecological footprint':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 7
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3'))

    if form_m2_ch3_q8.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(8)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q8.type.data, author=current_user)
        if moduls.question_str == 'The PHDI in country B is larger':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 8
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3'))

    if form_m2_ch3_q9.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(9)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q9.type.data, author=current_user)
        if moduls.question_str == 'It is closing the gap with the HDI':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 9
        moduls.question_option = 50
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3'))
    return render_template('se web/ch3/se_web_ch3.html', title='SE Web - ch3',
                           form_m2_ch3_q1=form_m2_ch3_q1, form_m2_ch3_q2=form_m2_ch3_q2,
                           form_m2_ch3_q3=form_m2_ch3_q3, form_m2_ch3_q4=form_m2_ch3_q4,
                           form_m2_ch3_q5=form_m2_ch3_q5, form_m2_ch3_q6=form_m2_ch3_q6,
                           form_m2_ch3_q7=form_m2_ch3_q7, form_m2_ch3_q8=form_m2_ch3_q8,
                           form_m2_ch3_q9=form_m2_ch3_q9)

#SE, Ch3, Exercise 1.
@se_module.route('/sustainable_energy_web/ch3/ex1', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex1():
    return render_template('se web/ch3/se_web_ch3_ex1.html', title='SE Web - ch3 - Ex1')

@se_module.route('/sustainable_energy_web/ch3/ex1/questionnaire', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex1_questionnaire():
    form_m2_ch3_e1 = ModulsForm_m2_ch3_e1()

    if form_m2_ch3_e1.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(11)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_e1.type.data, author=current_user)
        if moduls.question_str == 'At the beginning of the Agricultural Revolution 12.000–15.000 years ago':
            moduls.question_option = 1
        elif moduls.question_str == 'In 1945 after the detonation of the first atomic bomb':
            moduls.question_option = 2
        else:
            moduls.question_option = 3
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 11
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3_ex1_questionnaire'))
    return render_template('se web/ch3/se_web_ch3_ex1_questionnaire.html', title='SE Web - ch3 - Ex1',
                           form_m2_ch3_e1=form_m2_ch3_e1)

@se_module.route('/sustainable_energy_web/ch3/ex1/questionnaire/refresh', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex1_questionnaire_refresh():
    form_m2_ch3_e1 = ModulsForm_m2_ch3_e1()
    option_1 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
        filter(Moduls.question_option.is_(1)). \
        order_by(Moduls.question_num.asc()).count()

    option_2 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
        filter(Moduls.question_option.is_(2)). \
        order_by(Moduls.question_num.asc()).count()

    option_3 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
        filter(Moduls.question_option.is_(3)). \
        order_by(Moduls.question_num.asc()).count()
    return render_template('se web/ch3/se_web_ch3_ex1_questionnaire.html', title='SE Web - ch3 - Ex1',
                           option_1=option_1,option_2=option_2,option_3=option_3,
                           form_m2_ch3_e1=form_m2_ch3_e1)

@se_module.route('/sustainable_energy_web/ch3/ex1/chat', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex1_chat():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user,
                    chat_module='SE_ch3_ex1',
                    chat_group='Exercise 1')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('se_module.se_web_ch3_ex1_chat_query'))
    return render_template('se web/ch3/se_web_ch3_ex1_chat_create.html', title='SE Web - ch3 - Ex1',
                           form= form, legend='Sustainable Energy, Chapter 3, Exercise 1')

@se_module.route('/sustainable_energy_web/ch3/ex1/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex1_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch3_ex1')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('se web/ch3/se_web_ch3_ex1_chat_query.html', title='SE Web - ch3 - Ex1',
                           chats=chats, legend='Sustainable Energy, Chapter 3, Exercise 1')

#SE, Ch3, Exercise 2.
@se_module.route('/sustainable_energy_web/ch3/ex2', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex2():
    return render_template('se web/ch3/se_web_ch3_ex2.html', title='SE Web - ch3 - ex2')

@se_module.route('/sustainable_energy_web/ch3/ex2/questionnaire', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex2_questionnaire():
    form_m2_ch3_e2 = ModulsForm_m2_ch3_e2()

    if form_m2_ch3_e2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(11)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_e2.type.data, author=current_user)
        if moduls.question_str == 'Carbon emissions':
            moduls.question_option = 1
        elif moduls.question_str == 'Ecological Footprint':
            moduls.question_option = 2
        else:
            moduls.question_option = 3
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch3. Human Development for the Anthropocene'
        moduls.question_num = 11
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_module.se_web_ch3_ex2_questionnaire'))
    return render_template('se web/ch3/se_web_ch3_ex2_questionnaire.html', title='SE Web - ch3 - ex2',
                           form_m2_ch3_e2=form_m2_ch3_e2)

@se_module.route('/sustainable_energy_web/ch3/ex2/questionnaire/refresh', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex2_questionnaire_refresh():
    form_m2_ch3_e2 = ModulsForm_m2_ch3_e2()
    option_1 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
        filter(Moduls.question_option.is_(1)). \
        order_by(Moduls.question_num.asc()).count()

    option_2 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
        filter(Moduls.question_option.is_(2)). \
        order_by(Moduls.question_num.asc()).count()

    option_3 = Moduls.query.filter(Moduls.question_num.is_(11)). \
        filter(Moduls.title_mo.is_('Sustainable Energy')). \
        filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
        filter(Moduls.question_option.is_(3)). \
        order_by(Moduls.question_num.asc()).count()
    return render_template('se web/ch3/se_web_ch3_ex2_questionnaire.html', title='SE Web - ch3 - ex2',
                           option_1=option_1,option_2=option_2,option_3=option_3,
                           form_m2_ch3_e2=form_m2_ch3_e2)

@se_module.route('/sustainable_energy_web/ch3/ex2/chat', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex2_chat():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user,
                    chat_module='SE_ch3_ex2',
                    chat_group='Exercise 1')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('se_module.se_web_ch3_ex2_chat_query'))
    return render_template('se web/ch3/se_web_ch3_ex2_chat_create.html', title='SE Web - ch3 - ex2',
                           form= form, legend='Sustainable Energy, Chapter 3, Exercise 2')

@se_module.route('/sustainable_energy_web/ch3/ex2/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch3_ex2_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch3_ex2')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('se web/ch3/se_web_ch3_ex2_chat_query.html', title='SE Web - ch3 - ex2',
                           chats=chats, legend='Sustainable Energy, Chapter 3, Exercise 2')
