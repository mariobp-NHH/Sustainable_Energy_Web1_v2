import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from webse import app, db, bcrypt
from webse.forms import RegistrationForm, LoginForm, UpdateAccountForm, ChatForm, ChatFormUpdate, ChatQueryForm, ChatFormExercise, QuestionFormExercise
from webse.forms import AppStatisticsForm, SEStatisticsForm, AnnouncementForm
from webse.forms import ModulsForm_M1_Ch2_Q1, ModulsForm_M1_Ch2_Q2, ModulsForm_M1_Ch2_Q3, ModulsForm_M1_Ch2_Q4, ModulsForm_M1_Ch2_Q5
from webse.forms import ModulsForm_M1_Ch1_Q1, ModulsForm_M1_Ch1_Q2, ModulsForm_M1_Ch1_Q3
from webse.forms import ModulsForm_M2_Ch1_E1, ModulsForm_M2_Ch1_E2, ModulsForm_M2_Ch1_Q1, ModulsForm_M2_Ch1_Q2
from webse.forms import ModulsForm_M2_Ch2_E1, ModulsForm_M2_Ch2_Q1, ModulsForm_M2_Ch2_Q2, ModulsForm_M2_Ch2_Q3
from webse.models import User, Moduls, Announcement, Chat
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/home')
@app.route('/')
def home():

    total_pages_announcements = Announcement.query.count()
    total_pages_chats = Chat.query.count()
    total_pages = min (total_pages_announcements, total_pages_chats)
    max_pages_announcements = Announcement.query.count()/1
    max_pages_chats = Chat.query.count()/2
    max_pages=max(max_pages_announcements,max_pages_chats)
    min_pages = min(max_pages_announcements, max_pages_chats)
    page = request.args.get('page', 1, type=int)
    """
    if total_pages<page:
        announcements = Announcement.query.all()
        chats = Chat.query.all()
    elif total_pages_announcements<page and total_pages_chats>=page:
        announcements = Announcement.query.all()
        chats = Chat.query.order_by(Chat.date_posted.desc()).paginate(page=page, per_page=2)
    elif total_pages_announcements>=page and total_pages_chats<page:
        announcements = Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=page, per_page=1)
        chats = Chat.query.all()
        
    if page<=min_pages:
        announcements = Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=page, per_page=1)
        chats = Chat.query.order_by(Chat.date_posted.desc()).paginate(page=page, per_page=1)
    elif page>min_pages and max_pages>=page>max_pages_chats:
        announcements = Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=page, per_page=1)
        chats = Chat.query.order_by(Chat.date_posted.desc()).paginate(page=max_pages_chats, per_page=1)
    else:
        announcements = Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=max_pages_announcements, per_page=1)
        chats = Chat.query.order_by(Chat.date_posted.desc()).paginate(page=page, per_page=1)
    """
    announcements = Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=max_pages_announcements,
                                                                                          per_page=1)
    chats = Chat.query.order_by(Chat.date_posted.desc()).paginate(page=page, per_page=1)

    return render_template('home.html', chats=chats, announcements=announcements, title='Home',
                           total_pages_announcements=total_pages_announcements, total_pages_chats=total_pages_chats)


@app.route('/chat_web', methods=['GET', 'POST'])
@login_required
def chat_web():
    page = request.args.get('page', 1, type=int)
    form = ChatQueryForm()
    if form.validate_on_submit():
        input_chat_module=form.chat_module.data
        input_chat_group=form.chat_group.data
        chats = Chat.query.filter(Chat.chat_module.is_(input_chat_module)). \
            filter(Chat.chat_group.is_(input_chat_group)). \
            order_by(Chat.date_posted.desc()).paginate(page=page, per_page=1)
        flash('Your chat query has been created!', 'success')
        return render_template('chat_web.html', title='Chat Web',
                           form=form, legend='Chat Web', chats=chats)
    chats = Chat.query.filter(Chat.chat_module.is_('Home Chat')). \
                filter(Chat.chat_group.is_('Group 1')). \
                order_by(Chat.date_posted.desc()).paginate(page=page, per_page=1)

    return render_template('chat_web.html', title='Chat Web',
                           form=form, legend='Chat Web', chats=chats)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, course=form.course.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
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
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

#Chat functions
@app.route("/chat/new", methods=['GET', 'POST'])
@login_required
def new_chat():
    form = ChatForm()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user, chat_module=form.chat_module.data,
                     chat_group=form.chat_group.data)
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('chat_web'))
    return render_template('create_chat.html', title='New Chat',
                           form=form, legend='New Chat')

@app.route("/chat/<int:chat_id>")
def chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    return render_template('chat.html', title=chat.title, chat=chat)

@app.route("/chat/user/<string:username>")
def user_chats(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    chats = Chat.query.filter_by(author=user)\
        .order_by(Chat.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('user_chats.html', chats=chats, user=user)

@app.route("/chat/<int:chat_id>/update", methods=['GET', 'POST'])
@login_required
def update_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.author != current_user:
        abort(403)
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat.title = form.title.data
        chat.content = form.content.data
        db.session.commit()
        flash('Your chat has been updated!', 'success')
        return redirect(url_for('chat', chat_id=chat.id))
    elif request.method == 'GET':
        form.title.data = chat.title
        form.content.data = chat.content
    return render_template('create_chat_lecture.html', title='Update chat',
                           form=form, legend='Update chat')

@app.route("/chat/<int:chat_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.author != current_user:
        abort(403)
    db.session.delete(chat)
    db.session.commit()
    flash('Your chat has been deleted!', 'success')
    return redirect(url_for('chat_web'))

#Announcements functions
@app.route("/announcement/new", methods=['GET', 'POST'])
@login_required
def new_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(announcement)
        db.session.commit()
        flash('Your announcement has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_announcement.html', title='New Announcement',
                           form=form, legend='New Announcement')

@app.route("/announcement/<int:announcement_id>")
def announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    return render_template('announcement.html', title=announcement.title, announcement=announcement)

@app.route("/announcement/user/<string:username>")
def user_announcements(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    announcements = Announcement.query.filter_by(author=user)\
        .order_by(Announcement.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('user_announcements.html', announcements=announcements, user=user)

@app.route("/announcement/<int:announcement_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('announcement', announcement_id=announcement.id))
    elif request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
    return render_template('create_announcement.html', title='Update Announcement',
                           form=form, legend='Update Announcement')


@app.route("/announcement/<int:announcement_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(int(announcement_id))
    if announcement.author != current_user:
        abort(403)
    db.session.delete(announcement)
    db.session.commit()
    flash('Your announcement has been deleted!', 'success')
    return redirect(url_for('home'))

# App Calculator form
@app.route('/app_calculator')
def app_calculator():
	return render_template('app_calculator.html', title='App Calculator')

# App Calculator routine
@app.route('/send1', methods=['POST'])
def send(sum=sum):
	num1 = request.form.get("num1")
	num2 = request.form.get("num2")
	oper_name = request.form.get("operation")

	num1 = float(num1)
	num2 = float(num2)
	if oper_name == "add":
		oper_result = num1 + num2
	elif oper_name == "subtract":
		oper_result = num1 - num2
	elif oper_name == "multiply":
		oper_result = num1 * num2
	elif oper_name == "divide":
		oper_result = num1 / num2

	return render_template ('app_calculator.html', sum=oper_result)


@app.route('/teachers')
def teachers():
	return render_template('teachers.html', title='Teachers')


# App web
@app.route('/app_web')
@login_required
def app_web():
	return render_template('app web/app_web.html', title='App Web')


# App Module, Chapter 1.
@app.route('/app_web/ch1', methods=['GET', 'POST'])
@login_required
def app_web_ch1():
    form_M1_Ch1_Q1 = ModulsForm_M1_Ch1_Q1()
    form_M1_Ch1_Q2 = ModulsForm_M1_Ch1_Q2()
    form_M1_Ch1_Q3 = ModulsForm_M1_Ch1_Q3()

    if form_M1_Ch1_Q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user).\
            filter(Moduls.title_mo.is_('App Development')).\
            filter(Moduls.title_ch.is_('Ch1. Introduction')).\
            filter(Moduls.question_num.is_(1)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M1_Ch1_Q1.type.data, author=current_user)
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

    if form_M1_Ch1_Q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch1. Introduction')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M1_Ch1_Q2.type.data, author=current_user)
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

    if form_M1_Ch1_Q3.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch1. Introduction')). \
            filter(Moduls.question_num.is_(3)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M1_Ch1_Q3.type.data, author=current_user)
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
                           form_M1_Ch1_Q1=form_M1_Ch1_Q1, form_M1_Ch1_Q2=form_M1_Ch1_Q2,
                           form_M1_Ch1_Q3=form_M1_Ch1_Q3)

# App Module, Chapter 2.
@app.route('/app_web/ch2', methods=['GET', 'POST'])
@login_required
def app_web_ch2():
    form_M1_Ch2_Q1 = ModulsForm_M1_Ch2_Q1()
    form_M1_Ch2_Q2 = ModulsForm_M1_Ch2_Q2()
    form_M1_Ch2_Q3 = ModulsForm_M1_Ch2_Q3()
    form_M1_Ch2_Q4 = ModulsForm_M1_Ch2_Q4()
    form_M1_Ch2_Q5 = ModulsForm_M1_Ch2_Q5()

    if form_M1_Ch2_Q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(1)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M1_Ch2_Q1.question_str.data, author=current_user)
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

    if form_M1_Ch2_Q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M1_Ch2_Q2.type.data, author=current_user)
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

    if form_M1_Ch2_Q3.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(3)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M1_Ch2_Q3.type.data, author=current_user)
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

    if form_M1_Ch2_Q4.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(4)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M1_Ch2_Q4.type.data, author=current_user)
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

    if form_M1_Ch2_Q5.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_('Ch2. Installation')). \
            filter(Moduls.question_num.is_(5)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M1_Ch2_Q5.type.data, author=current_user)
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
                           form_M1_Ch2_Q1=form_M1_Ch2_Q1, form_M1_Ch2_Q2=form_M1_Ch2_Q2, form_M1_Ch2_Q3 = form_M1_Ch2_Q3,
                           form_M1_Ch2_Q4=form_M1_Ch2_Q4, form_M1_Ch2_Q5=form_M1_Ch2_Q5)

# Sustainable Energy Web
@app.route('/sustainable_energy_web')
@login_required
def sustainable_energy_web():
	return render_template('se web/sustainable_energy_web.html', title='SE Web')

# Sustainable Energy Module, Chapter 1.
@app.route('/sustainable_energy_web/ch1', methods=['GET', 'POST'])
@login_required
def se_web_ch1():
    form_M2_Ch1_Q1 = ModulsForm_M2_Ch1_Q1()
    form_M2_Ch1_Q2 = ModulsForm_M2_Ch1_Q2()

    if form_M2_Ch1_Q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch1. Overview')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M2_Ch1_Q1.type.data, author=current_user)
        if moduls.question_str == 'Should also consider social aspects':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch1. Overview'
        moduls.question_num = 2
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_web_ch1'))

    if form_M2_Ch1_Q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch1. Overview')). \
            filter(Moduls.question_num.is_(3)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M2_Ch1_Q2.type.data, author=current_user)
        if moduls.question_str == 'Sustainability and economy are a subsystem of the ecosystem':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch1. Overview'
        moduls.question_num = 3
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_web_ch1'))
    return render_template('se web/se_web_ch1.html', title='SE Web - Ch1',
                           form_M2_Ch1_Q1=form_M2_Ch1_Q1,
                           form_M2_Ch1_Q2=form_M2_Ch1_Q2)

@app.route('/sustainable_energy_web/ch1/ex1', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex1():
    form_M2_Ch1_E1 = ModulsForm_M2_Ch1_E1()
    form_chat = ChatFormExercise()
    form_question = QuestionFormExercise()

    if form_M2_Ch1_E1.validate_on_submit():
        #...
        return redirect(url_for('se_web_ch1_ex1'))

    return render_template('se web/se_web_ch1_ex1.html', title='SE Web - Ch1 - Ex1',
                           form_M2_Ch1_E1=form_M2_Ch1_E1, form_chat= form_chat,
                           form_question=form_question)

@app.route('/sustainable_energy_web/ch1/ex2', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex2():
    form_M2_Ch1_E2 = ModulsForm_M2_Ch1_E2()
    form_chat = ChatFormExercise()
    form_question = QuestionFormExercise()

    if form_M2_Ch1_E2.validate_on_submit():
        #...
        return redirect(url_for('se_web_ch1_ex2'))

    return render_template('se web/se_web_ch1_ex2.html', title='SE Web - Ch1 - Ex2',
                           form_M2_Ch1_E2=form_M2_Ch1_E2, form_chat= form_chat,
                           form_question=form_question)

# Sustainable Energy Module, Chapter 2.
@app.route('/sustainable_energy_web/ch2', methods=['GET', 'POST'])
@login_required
def se_web_ch2():
    form_M2_Ch2_Q1 = ModulsForm_M2_Ch2_Q1()
    form_M2_Ch2_Q2 = ModulsForm_M2_Ch2_Q2()
    form_M2_Ch2_Q3 = ModulsForm_M2_Ch2_Q3()

    if form_M2_Ch2_Q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user).\
            filter(Moduls.title_mo.is_('Sustainable Energy')).\
            filter(Moduls.title_ch.is_('Ch2. Ecological Footprint and Biocapacity')).\
            filter(Moduls.question_num.is_(1)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M2_Ch2_Q1.type.data, author=current_user)
        if moduls.question_str == 'Biologically productive area it takes to satisfy the demands of people':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Ecological Footprint and Biocapacity'
        moduls.question_num = 1
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_web_ch2'))

    if form_M2_Ch2_Q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch2. Wind')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M2_Ch2_Q2.type.data, author=current_user)
        if moduls.question_str == 'Local':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Wind'
        moduls.question_num = 2
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_web_ch2'))

    if form_M2_Ch2_Q3.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch2. Wind')). \
            filter(Moduls.question_num.is_(3)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_M2_Ch2_Q3.type.data, author=current_user)
        if moduls.question_str == 'Medium':
            moduls.question_result = 1
        else:
            moduls.question_result = 0
        moduls.title_mo = 'Sustainable Energy'
        moduls.title_ch = 'Ch2. Wind'
        moduls.question_num = 3
        db.session.add(moduls)
        db.session.commit()
        flash('Your answer has been submitted!', 'success')
        return redirect(url_for('se_web_ch2'))
    return render_template('se web/se_web_ch2.html', title='SE Web - Ch2',
                           form_M2_Ch2_Q1=form_M2_Ch2_Q1, form_M2_Ch2_Q2=form_M2_Ch2_Q2,
                           form_M2_Ch2_Q3=form_M2_Ch2_Q3)

@app.route('/sustainable_energy_web/ch2/ex1', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex1():
    form_M2_Ch2_E1 = ModulsForm_M2_Ch2_E1()
    form_chat = ChatFormExercise()
    form_question = QuestionFormExercise()

    if form_M2_Ch2_E1.validate_on_submit():
        #...
        return redirect(url_for('se_web_ch2_ex1'))

    return render_template('se web/se_web_ch2_ex1.html', title='SE Web - Ch2 - Ex1',
                           form_M2_Ch2_E1=form_M2_Ch2_E1, form_chat= form_chat,
                           form_question=form_question)


#Statistics
@app.route('/statistics', methods=['GET', 'POST'])
@login_required
def statistics():
    app_statistics_form = AppStatisticsForm()
    se_statistics_form = SEStatisticsForm()
    if app_statistics_form.validate_on_submit():
        app_statistics_input = app_statistics_form.type.data
        entries_app = Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_(app_statistics_input)). \
            order_by(Moduls.question_num.asc()).all()

        app_incorrect = Moduls.query.filter_by(author=current_user). \
            filter(Moduls.question_result.is_(0)). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_(app_statistics_input)). \
            order_by(Moduls.question_num.asc()).count()

        app_correct = Moduls.query.filter_by(author=current_user). \
            filter(Moduls.question_result.is_(1)). \
            filter(Moduls.title_mo.is_('App Development')). \
            filter(Moduls.title_ch.is_(app_statistics_input)). \
            order_by(Moduls.question_num.asc()).count()

        flash('Your answer has been submitted!', 'success')
        return render_template('statistics.html', app_statistics_form=app_statistics_form,
                               se_statistics_form=se_statistics_form, entries_app=entries_app,
                               app_correct=app_correct, app_incorrect=app_incorrect,
                               se_correct=0, se_incorrect=0)
    if se_statistics_form.validate_on_submit():
        se_statistics_input = se_statistics_form.type.data
        entries_se = Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_(se_statistics_input)). \
            order_by(Moduls.question_num.asc()).all()

        se_incorrect = Moduls.query.filter_by(author=current_user). \
            filter(Moduls.question_result.is_(0)). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_(se_statistics_input)). \
            order_by(Moduls.question_num.asc()).count()

        se_correct = Moduls.query.filter_by(author=current_user). \
            filter(Moduls.question_result.is_(1)). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_(se_statistics_input)). \
            order_by(Moduls.question_num.asc()).count()

        flash('Your answer has been submitted!', 'success')
        return render_template('statistics.html', app_statistics_form=app_statistics_form,
                               se_statistics_form=se_statistics_form, entries_se=entries_se,
                               app_correct=0, app_incorrect=0,
                               se_correct=se_correct, se_incorrect=se_incorrect)

    entries_app = Moduls.query.filter_by(author=current_user).filter(Moduls.title_mo.is_('---')).order_by(Moduls.date_exercise.desc()).all()
    entries_se = Moduls.query.filter_by(author=current_user).filter(Moduls.title_mo.is_('---')).order_by(
        Moduls.date_exercise.desc()).all()
    return render_template('statistics.html', app_statistics_form=app_statistics_form, se_statistics_form=se_statistics_form,
                           entries_app=entries_app, entries_se=entries_se,
                               app_correct=0, app_incorrect=0,
                               se_correct=0, se_incorrect=0)



#--Routes templates--#
@app.route('/sustainable_energy_web/ch2/ex1___', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex1___():
    form_M2_Ch2_E1___ = ModulsForm_M2_Ch2_E1___()
    form_chat = ChatFormExercise()
    form_question = QuestionFormExercise()

    if form_M2_Ch2_E1___.validate_on_submit():
        #...
        return redirect(url_for('se_web_ch2_ex1___'))

    return render_template('se web/se_web_ch2_ex1___.html', title='SE Web - Ch2 - Ex1___',
                           form_M2_Ch2_E1___=form_M2_Ch2_E1___, form_chat= form_chat,
                           form_question=form_question)