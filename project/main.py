import os
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone
from .models import User, Post
from flask import current_app as app

main = Blueprint('main', __name__)

db = SQLAlchemy()

@main.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main.route('/detail/<int:id>/')
def detail(id):
    post_id = Post.query.get(id)
    if post_id is None:
        abort(404)
    else:
        post = Post.query.filter_by(id=id).first()
        return render_template('detail.html', post=post)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', 
                            username=current_user.username, 
                            email=current_user.email)

@main.route('/go-postform')
@login_required
def go_postform():
    return render_template('create_post.html')

img_item = []

@main.route('/upload', methods=['POST'])
def handle_upload():
    for key, f in request.files.items():
        if key.startswith('file'):
            img_name = f.filename
            img_item.append(img_name)
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return '', 204

@main.route('/form', methods=['POST'])
def handle_form():
    title = request.form.get('title')
    content = request.form.get('content')
    user_id = current_user.id
    img_name = ''.join(img_item)
    newpost = Post(
        title=title, 
        content=content,
        user_id=user_id,
        img_name=img_name)
    db.session.add(newpost)
    db.session.commit()
    return redirect(url_for('main.index'))


