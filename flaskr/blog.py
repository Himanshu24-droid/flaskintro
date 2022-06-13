from flask import(
    Blueprint,url_for,render_template,flash,redirect,request
)
from werkzeug.exceptions import abort
from flask_login import current_user, login_required

from .extensions import db
from .models import User, Post, Comment

bp=Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = Post.query.all()
    comments = Comment.query.all()
    return render_template('blog/index.html', posts=posts,comments=comments)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        error=None

        if not title:
            error='Title is required'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title,body=body,author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post=Post.query.get_or_404(id)
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        error=None

        if not title:
            error='Title is required'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/comment', methods=('GET','POST'))
@login_required
def comment(id):
    p = Post.query.get_or_404(id)
    if request.method=='POST':
        comment=request.form['comment']
        error=None

        if not comment:
            error='Please type comment and try again.'

        if error is not None:
            flash(error)
        else:
            cmnt = Comment(comment=comment,user_name=current_user.username,post=p)
            db.session.add(cmnt)
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/comment.html')

@bp.route('/<int:id>/delete_comment', methods=('POST',))
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('blog.index'))