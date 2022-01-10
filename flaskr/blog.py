from flask import(
    Blueprint,url_for,render_template,flash,g,redirect,request,g
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp=Blueprint('blog', __name__)

@bp.route('/')
def index():
    try:
        db=get_db()
        posts=db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
        ).fetchall()
        comments=db.execute(
            'SELECT c.id, comment, created, user_name, post_id '
            ' FROM comment c JOIN user u ON c.user_name = u.username'
            ' ORDER BY created ASC'
        ).fetchall()
    except sqlite3.OperationalError:
        flash('You have no database.')

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
            db=get_db()
            db.execute(
                'INSERT INTO post (title,body,author_id)'
                'VALUES (?,?,?)',
                (title,body,g.user['id']),
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post=get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,),
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post=get_post(id)
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        error=None

        if not title:
            error='Title is required'

        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id=?',
                (title,body,id),
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db=get_db()
    db.execute('DELETE FROM post WHERE id=?',(id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/comment', methods=('GET','POST'))
@login_required
def comment(id):
    post=get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,),
    ).fetchone()
    if request.method=='POST':
        comment=request.form['comment']
        error=None

        if not comment:
            error='Please type comment and try again.'

        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute(
                'INSERT INTO comment (comment,user_name,post_id)'
                'VALUES (?,?,?)',
                (comment,g.user['username'],post['id'],),
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/comment.html')

@bp.route('/<int:id>/delete_comment', methods=('POST',))
@login_required
def delete_comment(id):
    db=get_db()
    comment=db.execute(
        'SELECT c.id, comment, created, user_name, post_id '
        ' FROM comment c JOIN user u ON c.user_name = u.username'
        ' WHERE c.id = ?',
        (id,),
    ).fetchone()
    db.execute('DELETE FROM comment WHERE id=?',(id,))
    db.commit()
    return redirect(url_for('blog.index'))