from .extensions import db
from datetime import datetime
from flask_login import UserMixin

'''user_posts = db.Table('user_posts',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

post_comments = db.Table('post_comments',
    db.Column('user_name', db.String(50), db.ForeignKey('post.author')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))'''

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #associate = db.relationship('Association',back_populates='post')
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return '<Post %r>' % self.title

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_name = db.Column(db.String(50), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.comment

'''class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)

    user = db.relationship('User', back_populates='associate')
    post = db.relationship('Post', back_populates='associate')
    comment = db.relationship('Comment')'''

