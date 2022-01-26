import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from webse import app, db, bcrypt
from webse.forms import RegistrationForm, LoginForm, UpdateAccountForm, ChatFormUpdate, AnnouncementForm
from webse.forms import ModulsForm_m1_ch2_q1, ModulsForm_m1_ch2_q2, ModulsForm_m1_ch2_q3, ModulsForm_m1_ch2_q4, ModulsForm_m1_ch2_q5
from webse.forms import ModulsForm_m1_ch1_q1, ModulsForm_m1_ch1_q2, ModulsForm_m1_ch1_q3
from webse.forms import ModulsForm_m2_ch1_e1, ModulsForm_m2_ch1_e2, ModulsForm_m2_ch1_q1, ModulsForm_m2_ch1_q2
from webse.forms import ModulsForm_m2_ch2_e1, ModulsForm_m2_ch2_e2, ModulsForm_m2_ch2_e3, ModulsForm_m2_ch2_q1, ModulsForm_m2_ch2_q2
from webse.forms import ModulsForm_m2_ch2_q3, ModulsForm_m2_ch2_q4, ModulsForm_m2_ch2_q5, ModulsForm_m2_ch2_q6, ModulsForm_m2_ch2_q7, ModulsForm_m2_ch2_q8
from webse.forms import ModulsForm_m2_ch3_e1, ModulsForm_m2_ch3_e2, ModulsForm_m2_ch3_e3, ModulsForm_m2_ch3_q1, ModulsForm_m2_ch3_q2
from webse.forms import ModulsForm_m2_ch3_q3, ModulsForm_m2_ch3_q4, ModulsForm_m2_ch3_q5, ModulsForm_m2_ch3_q6, ModulsForm_m2_ch3_q7, ModulsForm_m2_ch3_q8
from webse.models import User, Moduls, Announcement, Chat
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/home')
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    announcements = Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=page, per_page=1)
    return render_template('home.html', announcements=announcements, title='Home')

######################################
####   Block 1. User Information   ###
######################################

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
    return render_template('user/register.html', title='Register', form=form)

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
    return render_template('user/login.html', title='Login', form=form)


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
    return render_template('user/account.html', title='Account',
                           image_file=image_file, form=form)

##################################
####   Block 2. Announcement   ###
###################################
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
    return render_template('announcement/create_announcement.html', title='New Announcement',
                           form=form, legend='New Announcement')

@app.route("/announcement/<int:announcement_id>")
def announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    return render_template('announcement/announcement.html', title=announcement.title, announcement=announcement)

@app.route("/announcement/user/<string:username>")
def user_announcements(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    announcements = Announcement.query.filter_by(author=user)\
        .order_by(Announcement.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('announcement/user_announcements.html', announcements=announcements, user=user)

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
    return render_template('announcement/create_announcement.html', title='Update Announcement',
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

##################################
####   Block 3. Query chat    ####
##################################

@app.route('/chat_web', methods=['GET', 'POST'])
@login_required
def chat_web():
    return render_template('chat/chat_web.html', title='Chat Web')

@app.route('/chat_web/chat_home')
@login_required
def chat_web_chat_home():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('Home Chat')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('chat/chat_home.html', chats=chats, title=' Chat Home', legend='Home Chat')

@app.route('/chat_web/chat_app_g1')
@login_required
def chat_web_chat_app_g1():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('App Module Chat')).\
        filter(Chat.chat_group.is_('Group 1')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('chat/chat_app_g1.html', chats=chats, title=' Chat App G1', legend='App Module Chat, Group 1')

@app.route('/chat_web/chat_app_g2')
@login_required
def chat_web_chat_app_g2():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('App Module Chat')).\
        filter(Chat.chat_group.is_('Group 2')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('chat/chat_app_g2.html', chats=chats, title=' Chat App G2', legend='App Module Chat, Group 2')

@app.route('/chat_web/chat_app_g3')
@login_required
def chat_web_chat_app_g3():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('App Module Chat')).\
        filter(Chat.chat_group.is_('Group 3')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('chat/chat_app_g3.html', chats=chats, title=' Chat App G3', legend='App Module Chat, Group 3')

@app.route('/chat_web/chat_app_g4')
@login_required
def chat_web_chat_app_g4():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('App Module Chat')).\
        filter(Chat.chat_group.is_('Group 4')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('chat/chat_app_g4.html', chats=chats, title=' Chat App G4', legend='App Module Chat, Group 4')

@app.route('/chat_web/chat_se_g1')
@login_required
def chat_web_chat_se_g1():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('Sustainable Energy Module Chat')).\
        filter(Chat.chat_group.is_('Group 1')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('chat/chat_se_g1.html', chats=chats, title=' Chat SE G1', legend='Sustainable Energy Module Chat, Group 1')

@app.route('/chat_web/chat_se_g2')
@login_required
def chat_web_chat_se_g2():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('Sustainable Energy Module Chat')).\
        filter(Chat.chat_group.is_('Group 2')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('chat/chat_se_g2.html', chats=chats, title=' Chat SE G2', legend='Sustainable Energy Module Chat, Group 2')

###################################################
####   Block 4. Create, update, delete chat    ####
###################################################

@app.route("/chat_new", methods=['GET', 'POST'])
@login_required
def new_chat():
    return render_template('chat/new_chat.html', title='Chat Web')

@app.route("/chat_new/create/home", methods=['GET', 'POST'])
@login_required
def new_chat_create_home():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user, chat_module='Home Chat',
                     chat_group='All')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('chat_web'))
    return render_template('chat/create_chat_home.html', title='Create Chat', form=form,legend='Home Chat')

@app.route("/chat_new/create/app_g1", methods=['GET', 'POST'])
@login_required
def new_chat_create_app_g1():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user, chat_module='App Module Chat',
                     chat_group='Group 1')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('chat_web'))
    return render_template('chat/create_chat_app_g1.html', title='Create Chat', form=form, legend='App Module Chat, Group 1')

@app.route("/chat_new/create/app_g2", methods=['GET', 'POST'])
@login_required
def new_chat_create_app_g2():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user, chat_module='App Module Chat',
                     chat_group='Group 2')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('chat_web'))
    return render_template('chat/create_chat_app_g3.html', title='Create Chat', form=form, legend='App Module Chat, Group 2')

@app.route("/chat_new/create/app_g3", methods=['GET', 'POST'])
@login_required
def new_chat_create_app_g3():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user, chat_module='App Module Chat',
                     chat_group='Group 3')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('chat_web'))
    return render_template('chat/create_chat_app_g3.html', title='Create Chat', form=form, legend='App Module Chat, Group 3')

@app.route("/chat_new/create/app_g4", methods=['GET', 'POST'])
@login_required
def new_chat_create_app_g4():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user, chat_module='App Module Chat',
                     chat_group='Group 4')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('chat_web'))
    return render_template('chat/create_chat_app_g4.html', title='Create Chat', form=form, legend='App Module Chat, Group 4')

@app.route("/chat_new/create/se_g1", methods=['GET', 'POST'])
@login_required
def new_chat_create_se_g1():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user, chat_module='Sustainable Energy Module Chat',
                     chat_group='Group 1')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('chat_web'))
    return render_template('chat/create_chat_se_g1.html', title='Create Chat', form=form, legend='Sustainable Energy Module Chat, Group 1')


@app.route("/chat_new/create/se_g2", methods=['GET', 'POST'])
@login_required
def new_chat_create_se_g2():
    form = ChatFormUpdate()
    if form.validate_on_submit():
        chat = Chat(title=form.title.data, content=form.content.data, author=current_user, chat_module='Sustainable Energy Module Chat',
                     chat_group='Group 2')
        db.session.add(chat)
        db.session.commit()
        flash('Your chat has been created!', 'success')
        return redirect(url_for('chat_web'))
    return render_template('chat/create_chat_se_g2.html', title='Create Chat', form=form, legend='Sustainable Energy Module Chat, Group 2')

@app.route("/chat/<int:chat_id>")
def chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    return render_template('chat/chat.html', title=chat.title, chat=chat)

@app.route("/chat/user/<string:username>")
def user_chats(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    chats = Chat.query.filter_by(author=user)\
        .order_by(Chat.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('chat/user_chats.html', chats=chats, user=user)

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
    return render_template('chat/create_chat_lecture.html', title='Update chat',
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

#####################################
####   Block 5. App Calculator   ####
#####################################

@app.route('/app_calculator')
def app_calculator():
    return render_template('app_calculator.html', title='App Calculator')

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

####################################
####   Block 6. Students Apps   ####
####################################

######################################
####   Block 7. Students thesis   ####
######################################


###############################
####   Block 8. Teachers   ####
###############################
@app.route('/teachers')
def teachers():
	return render_template('teachers.html', title='Teachers')


#################################
####   Block 9. App Module   ####
#################################
# App web
@app.route('/app_web')
@login_required
def app_web():
	return render_template('app web/app_web.html', title='App Web')

# App Module, Chapter 1.
@app.route('/app_web/ch1', methods=['GET', 'POST'])
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
@app.route('/app_web/ch2', methods=['GET', 'POST'])
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

#################################################
####   Block 10. Sustainable Energy Module   ####
#################################################
@app.route('/sustainable_energy_web')
@login_required
def sustainable_energy_web():
	return render_template('se web/sustainable_energy_web.html', title='SE Web')

##########################################
## Sustainable Energy Module, Chapter 1 ##
##########################################
@app.route('/sustainable_energy_web/ch1', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch1'))

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
        return redirect(url_for('se_web_ch1'))
    return render_template('se web/ch1/se_web_ch1.html', title='SE Web - Ch1',
                           form_m2_ch1_q1=form_m2_ch1_q1,
                           form_m2_ch1_q2=form_m2_ch1_q2)

#SE, Ch1, Exercise 1.
@app.route('/sustainable_energy_web/ch1/ex1', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex1():
    return render_template('se web/ch1/se_web_ch1_ex1.html', title='SE Web - Ch1 - Ex1')

@app.route('/sustainable_energy_web/ch1/ex1/questionnaire', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch1_ex1_questionnaire'))
    return render_template('se web/ch1/se_web_ch1_ex1_questionnaire.html', title='SE Web - Ch1 - Ex1',
                           form_m2_ch1_e1=form_m2_ch1_e1)

@app.route('/sustainable_energy_web/ch1/ex1/questionnaire/refresh', methods=['GET', 'POST'])
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


@app.route('/sustainable_energy_web/ch1/ex1/chat', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch1_ex1_chat_query'))
    return render_template('se web/ch1/se_web_ch1_ex1_chat_create.html', title='SE Web - Ch1 - Ex1',
                           form= form, legend='Sustainable Energy, Chapter 1, Exercise 1')

@app.route('/sustainable_energy_web/ch1/ex1/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex1_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch1_ex1')).order_by(Chat.date_posted.desc()).paginate(page=page,
                                                                                                            per_page=4)
    return render_template('se web/ch1/se_web_ch1_ex1_chat_query.html', title='SE Web - Ch1 - Ex1',
                           chats=chats, legend='Sustainable Energy, Chapter 1, Exercise 1')

#SE, Ch1, Exercise 2.
@app.route('/sustainable_energy_web/ch1/ex2', methods=['GET', 'POST'])
@login_required
def se_web_ch1_ex2():
    return render_template('se web/ch1/se_web_ch1_ex2.html', title='SE Web - Ch1 - ex2')

@app.route('/sustainable_energy_web/ch1/ex2/questionnaire', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch1_ex2_questionnaire'))
    return render_template('se web/ch1/se_web_ch1_ex2_questionnaire.html', title='SE Web - Ch1 - ex2',
                           form_m2_ch1_e2=form_m2_ch1_e2)

@app.route('/sustainable_energy_web/ch1/ex2/questionnaire/refresh', methods=['GET', 'POST'])
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

@app.route('/sustainable_energy_web/ch1/ex2/chat', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch1_ex2_chat_query'))
    return render_template('se web/ch1/se_web_ch1_ex2_chat_create.html', title='SE Web - Ch1 - Ex2',
                           form= form, legend='Sustainable Energy, Chapter 1, Exercise 2')

@app.route('/sustainable_energy_web/ch1/ex2/chat/query', methods=['GET', 'POST'])
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
@app.route('/sustainable_energy_web/ch2', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch2'))

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
        return redirect(url_for('se_web_ch2'))

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
        return redirect(url_for('se_web_ch2'))

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
        return redirect(url_for('se_web_ch2'))

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
        return redirect(url_for('se_web_ch2'))

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
        return redirect(url_for('se_web_ch2'))

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
        return redirect(url_for('se_web_ch2'))

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
        return redirect(url_for('se_web_ch2'))
    return render_template('se web/ch2/se_web_ch2.html', title='SE Web - Ch2',
                           form_m2_ch2_q1=form_m2_ch2_q1, form_m2_ch2_q2=form_m2_ch2_q2,
                           form_m2_ch2_q3=form_m2_ch2_q3, form_m2_ch2_q4=form_m2_ch2_q4,
                           form_m2_ch2_q5=form_m2_ch2_q5, form_m2_ch2_q6=form_m2_ch2_q6,
                           form_m2_ch2_q7=form_m2_ch2_q7, form_m2_ch2_q8=form_m2_ch2_q8)

#SE, Ch2, Exercise 1.
@app.route('/sustainable_energy_web/ch2/ex1', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex1():
    return render_template('se web/ch2/se_web_ch2_ex1.html', title='SE Web - ch2 - Ex1')

@app.route('/sustainable_energy_web/ch2/ex1/questionnaire', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch2_ex1_questionnaire'))
    return render_template('se web/ch2/se_web_ch2_ex1_questionnaire.html', title='SE Web - ch2 - Ex1',
                           form_m2_ch2_e1=form_m2_ch2_e1)

@app.route('/sustainable_energy_web/ch2/ex1/questionnaire/refresh', methods=['GET', 'POST'])
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

@app.route('/sustainable_energy_web/ch2/ex1/chat', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch2_ex1_chat_query'))
    return render_template('se web/ch2/se_web_ch2_ex1_chat_create.html', title='SE Web - ch2 - Ex1',
                           form= form, legend='Sustainable Energy, Chapter 2, Exercise 1')

@app.route('/sustainable_energy_web/ch2/ex1/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex1_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch2_ex1')).order_by(Chat.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('se web/ch2/se_web_ch2_ex1_chat_query.html', title='SE Web - ch2 - Ex1',
                           chats=chats, legend='Sustainable Energy, Chapter 2, Exercise 1')

#SE, Ch2, Exercise 2.
@app.route('/sustainable_energy_web/ch2/ex2', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex2():
    return render_template('se web/ch2/se_web_ch2_ex2.html', title='SE Web - ch2 - ex2')

@app.route('/sustainable_energy_web/ch2/ex2/questionnaire', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch2_ex2_questionnaire'))
    return render_template('se web/ch2/se_web_ch2_ex2_questionnaire.html', title='SE Web - ch2 - ex2',
                           form_m2_ch2_e2=form_m2_ch2_e2)

@app.route('/sustainable_energy_web/ch2/ex2/questionnaire/refresh', methods=['GET', 'POST'])
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

@app.route('/sustainable_energy_web/ch2/ex2/chat', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch2_ex2_chat_query'))
    return render_template('se web/ch2/se_web_ch2_ex2_chat_create.html', title='SE Web - ch2 - ex2',
                           form= form, legend='Sustainable Energy, Chapter 2, Exercise 2')

@app.route('/sustainable_energy_web/ch2/ex2/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex2_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch2_ex2')).order_by(Chat.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template('se web/ch2/se_web_ch2_ex2_chat_query.html', title='SE Web - ch2 - ex2',
                           chats=chats, legend='Sustainable Energy, Chapter 2, Exercise 2')

#SE, Ch2, Exercise 3.
@app.route('/sustainable_energy_web/ch2/ex3', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex3():
    return render_template('se web/ch2/se_web_ch2_ex3.html', title='SE Web - ch2 - ex3')

@app.route('/sustainable_energy_web/ch2/ex3/questionnaire', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch2_ex3_questionnaire'))

    return render_template('se web/ch2/se_web_ch2_ex3_questionnaire.html', title='SE Web - ch2 - ex3',
                           form_m2_ch2_e3=form_m2_ch2_e3)

@app.route('/sustainable_energy_web/ch2/ex3/questionnaire/refresh', methods=['GET', 'POST'])
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

@app.route('/sustainable_energy_web/ch2/ex3/chat', methods=['GET', 'POST'])
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
        return redirect(url_for('se_web_ch2_ex3_chat_query'))
    return render_template('se web/ch2/se_web_ch2_ex3_chat_create.html', title='SE Web - ch2 - ex3',
                           form= form, legend='Sustainable Energy, Chapter 2, Exercise 3')

@app.route('/sustainable_energy_web/ch2/ex3/chat/query', methods=['GET', 'POST'])
@login_required
def se_web_ch2_ex3_chat_query():
    page = request.args.get('page', 1, type=int)
    chats = Chat.query.filter(Chat.chat_module.is_('SE_ch2_ex3')).order_by(Chat.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template('se web/ch2/se_web_ch2_ex3_chat_query.html', title='SE Web - ch2 - ex3',
                           chats=chats, legend='Sustainable Energy, Chapter 2, Exercise 3')

##########################################
## Sustainable Energy Module, Chapter 3 ##
##########################################
@app.route('/sustainable_energy_web/ch3', methods=['GET', 'POST'])
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

    if form_m2_ch3_q1.validate_on_submit():
        Moduls.query.filter_by(author=current_user).\
            filter(Moduls.title_mo.is_('Sustainable Energy')).\
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')).\
            filter(Moduls.question_num.is_(1)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q1.type.data, author=current_user)
        if moduls.question_str == 'Biologically productive area it takes to satisfy the demands of people':
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
        return redirect(url_for('se_web_ch3'))

    if form_m2_ch3_q2.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(2)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q2.type.data, author=current_user)
        if moduls.question_str == 'Land and sea area available to provide the resources a population consumes and to absorb its wastes':
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
        return redirect(url_for('se_web_ch3'))

    if form_m2_ch3_q3.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(3)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q3.type.data, author=current_user)
        if moduls.question_str == 'Both':
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
        return redirect(url_for('se_web_ch3'))

    if form_m2_ch3_q4.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(4)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q4.type.data, author=current_user)
        if moduls.question_str == 'Both':
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
        return redirect(url_for('se_web_ch3'))

    if form_m2_ch3_q5.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(5)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q5.type.data, author=current_user)
        if moduls.question_str == 'Reflect the relative productivity of a given land use type':
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
        return redirect(url_for('se_web_ch3'))

    if form_m2_ch3_q6.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(6)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q6.type.data, author=current_user)
        if moduls.question_str == 'Very suitable, suitable, moderately suitable, marginally suitable, and not suitable':
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
        return redirect(url_for('se_web_ch3'))

    if form_m2_ch3_q7.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(7)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q7.type.data, author=current_user)
        if moduls.question_str == 'In the 70s':
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
        return redirect(url_for('se_web_ch3'))

    if form_m2_ch3_q8.validate_on_submit():
        Moduls.query.filter_by(author=current_user). \
            filter(Moduls.title_mo.is_('Sustainable Energy')). \
            filter(Moduls.title_ch.is_('Ch3. Human Development for the Anthropocene')). \
            filter(Moduls.question_num.is_(8)).delete()
        db.session.commit()
        moduls = Moduls(question_str=form_m2_ch3_q8.type.data, author=current_user)
        if moduls.question_str == 'It represents the 60%':
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
        return redirect(url_for('se_web_ch3'))
    return render_template('se web/ch3/se_web_ch3.html', title='SE Web - ch3',
                           form_m2_ch3_q1=form_m2_ch3_q1, form_m2_ch3_q2=form_m2_ch3_q2,
                           form_m2_ch3_q3=form_m2_ch3_q3, form_m2_ch3_q4=form_m2_ch3_q4,
                           form_m2_ch3_q5=form_m2_ch3_q5, form_m2_ch3_q6=form_m2_ch3_q6,
                           form_m2_ch3_q7=form_m2_ch3_q7, form_m2_ch3_q8=form_m2_ch3_q8)


##################################
####   Block 11. Statistics   ####
##################################

@app.route('/statistics', methods=['GET', 'POST'])
@login_required
def statistics():
    entries = Moduls.query.filter_by(author=current_user).filter(Moduls.title_mo.is_('---')).order_by(Moduls.date_exercise.desc()).all()
    return render_template('statistics/statistics.html',entries=entries, correct=0, incorrect=0)

@app.route('/statistics/se_ch1', methods=['GET', 'POST'])
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

@app.route('/statistics/se_ch2', methods=['GET', 'POST'])
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

