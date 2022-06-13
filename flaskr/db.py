import click
from flask.cli import with_appcontext
from .extensions import db
from .models import User,Post,Comment

def init_db():
    db.create_all()

def close_db():
    db.drop_all()

@click.command(name='init-db')
@with_appcontext
def create_tables():
    close_db()
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(create_tables)