from flask import render_template, redirect, url_for, abort, flash
from datetime import timedelta, datetime, date
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, NewProjectForm, EditProjectAdminForm
from .. import db
from ..models import Permission, Role, User, Project
from ..decorators import admin_required


@main.route('/')
def index():
    projects = Project.query.filter_by(approved=True).order_by(Project.timestamp.desc()).all()
    today = datetime.now()
    return render_template('index.html', projects=projects, today=today)

@main.route('/create', methods=['GET', 'POST'])
def create():
    form = NewProjectForm()
    if form.validate_on_submit():
        project = Project(who=form.who.data,
                        what=form.what.data,
                        couse=form.couse.data,
                        organization_name=form.organization_name.data,
                        organization_url=form.organization_url.data,
                        about=form.about.data,
                        author=current_user._get_current_object())
        db.session.add(project)
        db.session.commit()
        flash('Thanks, you will ricive a mail when your prject be approved.')
        return redirect(url_for('main.index')) 
    flash('something is wrong')
    return render_template('create.html', form=form) 

@main.route('/bribes/<int:id>', methods=['GET', 'POST'])
def project(id):
    project = Project.query.get(id)
    form = EditProjectAdminForm(project=project)
    if form.validate_on_submit():
        project.who = form.who.data
        project.what = form.what.data
        project.couse = form.couse.data
        project.organization_name = form.organization_name.data
        organization_url = form.organization_url.data
        project.about = form.about.data     
        project.approved = form.approved.data
        db.session.add(project)
        flash('The profile has been updated.')
        return redirect(url_for('main.index')) 
    form.who.data = project.who
    form.what.data = project.what
    form.couse.data = project.couse
    form.organization_name.data = project.organization_name
    form.organization_url.data = project.organization_url
    form.about.data = project.about
    form.approved.data = project.approved
    return render_template('admin/approve_project.html', projects=[project], project=project, form=form)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/admin/approve', methods=['GET', 'POST'])
@admin_required
def admin_approve():
    projects = Project.query.order_by(Project.timestamp.desc()).all()
    today = datetime.now()
    return render_template('admin/approve.html', projects=projects, today=today)
