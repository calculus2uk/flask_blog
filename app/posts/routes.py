from flask import Blueprint, current_app, g
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request
from app.models import Post, db
from app.posts import posts # blueprints
from app.posts.forms import PostForm
from app.main.forms import SearchForm

@posts.before_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@posts.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'] , False)
    return render_template('index.html', title='Explore', posts=posts)


@posts.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
 	form = PostForm()
 	if form.validate_on_submit():
 		post = Post(title=form.title.data, body=form.post.data, author=current_user)
 		db.session.add(post)
 		db.session.commit()
 		flash('Your post is now live!')
 		return redirect(url_for('main.index'))
 	return render_template("new_post.html", title='Home Page', form=form)
