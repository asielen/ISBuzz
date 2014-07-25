#!/usr/bin/env python
import os

from app import create_app, db
from app.models import User, Role, Permission, Region
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Region=Region, Role=Role, Permission=Permission)
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def setuptest():
    """ Set enviromental variables from keys.ini"""

    import configparser
    from app import db

    # Set Enviromental variables
    cfig = configparser.ConfigParser()
    cfig.read('keys.ini')
    os.environ['SECRET_KEY'] = cfig['KEYS']['secret_key']
    os.environ['MAIL_USERNAME'] = cfig['KEYS']['mail_username']
    os.environ['MAIL_PASSWORD'] = cfig['KEYS']['mail_password']
    os.environ['FLASKY_ADMIN'] = cfig['KEYS']['owner_email']
    if os.environ.get('SECRET_KEY') == "" or os.environ.get('MAIL_USERNAME') == "" \
        or os.environ.get('MAIL_PASSWORD') == "" or os.environ.get('FLASKY_ADMIN') == "":
        raise EnvironmentError

    # Setup Database Tables
    db.create_all()


@manager.command
def deploy():
    """Run deployment tasks."""
    from app.models import Role, Region

    # create user roles
    Role.insert_roles()

    # create regions
    Region.insert_regions()


if __name__ == '__main__':
    manager.run()
