from flask import Flask, url_for, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_admin import Admin, helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore, user_registered
from werkzeug.security import generate_password_hash
from datetime import datetime


mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
moment = Moment()
login.login_view = 'users.login'

admin = Admin()
security = Security()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    admin.init_app(app)

    # Setup Flask-Security
    from app.models import User, Role, roles_users
    from app.secu.forms import ExtendedRegisterForm, ExtendedLoginForm
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    ##registration and login FORM both modified to suit my implementation
    security_ctx = security.init_app(app, datastore, register_form=ExtendedRegisterForm, login_form=ExtendedLoginForm)


    @security_ctx.context_processor
    def security_context_processor():
        return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for)

    with app.app_context():
        db.drop_all()
        db.create_all()

    # this route is fired when a user registers, a role is assingned to 
    # the user as admin or normal_user
    @user_registered.connect_via(app)
    def user_registered_sighandler(app, user, confirm_token):
        role = Role.query.filter_by(name="Normal_User").first()
        
        if role is None:
            role = Role(name="Normal_User", description="Normal User")
            db.session.add(role)
            db.session.commit()
        datastore.add_role_to_user(user, role)

        if user.email == app.config['ADMIN_EMAIL']:
            super_role = Role.query.filter_by(name="Admin").first()
            if super_role is None:
                super_role = Role(name=app.config['ADMIN_ROLE'], description="Administrator")
                db.session.add(super_role)
                db.session.commit()
            datastore.add_role_to_user(user, role)
            datastore.add_role_to_user(user, super_role)


   #email server configurations
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)


    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    from app.users import users
    @users.context_processor
    def security_context_processor():
        return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for)


    app.register_blueprint(users)

    from app.posts import posts
    app.register_blueprint(posts)

    from app.main import main
    app.register_blueprint(main, template_folder='templates')

    from app.errors import errors
    app.register_blueprint(errors)


    return app

from app import models