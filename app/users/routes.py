from flask import current_app
from flask import render_template, flash, redirect, url_for, request
from app.secu.forms import ExtendedRegisterForm, ExtendedLoginForm
from flask_security import current_user, logout_user, login_required, login_user
from werkzeug.urls import url_parse
from app.models import User, db
from app.users import users


## This routes are handled by flask_security and I dont need to define them again
# @users.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     register_user_form = ExtendedRegisterForm()
#     if register_user_form.validate_on_submit():
#         print('hi thee')
#         user = User(username=register_user_form.username.data, email=register_user_form.email.data)
#         user.set_password(register_user_form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('users.login'))
#     return render_template('register.html', title='Register', register_user_form=register_user_form)


# @users.route('/login', methods=['GET', 'POST'])
# def login():
# 	if current_user.is_authenticated:
# 		return redirect(url_for('main.index'))
# 	form = ExtendedLoginForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(username=form.username.data).first()
# 		if user is None or not user.check_password(form.password.data):
# 			flash('Invalid username or password')
# 			return redirect(url_for('users.login'))
# 		login_user(user, remember=form.remember.data)
# 		next_page = request.args.get('next')
# 		if not next_page or url_parse(next_page).netloc != '':
# 			next_page = url_for('main.index')
# 		return redirect(next_page)
# 	return render_template('security/login_user.html', title='Sign In', login_user_form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

	
@users.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    page = request.args.get('page', 1, type=int)
    posts = current_user.posts.paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template('users/user.html', user=user, posts=posts, image_file=image_file)


@users.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('users.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html', title='Edit Profile',
                           form=form)


@users.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('users.user', username=username))

@users.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('users.user', username=username))
