from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..decorators import admin_required
from ..models import Permission, Role, User


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
    chart = ""
    if current_user.is_authenticated():
        pass
        #show_followed = bool(request.cookies.get('show_followed', ''))
    return render_template('index.html', chart=chart)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # # form = EditProfileForm()
    # # if form.validate_on_submit():
    # #     current_user.name = form.name.data
    # #     current_user.location = form.location.data
    # #     current_user.about_me = form.about_me.data
    # #     db.session.add(current_user)
    # #     flash('Your profile has been updated.')
    # #     return redirect(url_for('.user', username=current_user.username))
    # form.name.data = current_user.name
    # form.location.data = current_user.location
    # form.about_me.data = current_user.about_me
    return render_template('edit_profile.html') #,form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.region = Role.query.get(form.region.data)
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.region.data = user.region
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/qualify/<username>', methods=['POST'])
@login_required
def new_sql(username):
    print(username)
    if current_user.username == username:
        flash('You qualified someone')
        print("You qualified someone'")
    else:
        flash('You are not logged in properly, please logout and try again')
        print("You are not logged in properly, please logout and try again")
    print("check")
    return "Yay, you qualified someone!"

