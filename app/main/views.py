from flask import render_template, redirect, url_for, abort, flash, request, session, \
escape, g, make_response
from datetime import timedelta, datetime, date
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, NewProjectForm1, EditProjectAdminForm, \
PaymentCheckout, LoginForm, RegistrationForm, AmountForm, NewProjectForm2
from .. import db
from ..models import Permission, Role, User, Project
from ..decorators import admin_required
import os, stripe

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


@main.route('/chellenge/<int:id>/donate', methods=['GET', 'POST'])
def donate(id):
    if current_user.is_anonymous():
        return redirect(url_for('main.donate_login_required', id=id))
    return render_template('donate.html', key=stripe_keys['publishable_key'], id=id)

@main.route('/chellenge/<int:id>/donate/amount', methods=['GET', 'POST'])
def amount(id):
    if current_user.is_anonymous():
        return redirect(url_for('main.donate_login_required', id=id))
    form = AmountForm()
    if form.validate_on_submit():
        amount = form.amount.data
        session['amount'] = amount
        return redirect(url_for('main.donate', id=id))
    return render_template('amount.html', form=form)

@main.route('/chellenge/<int:id>/charge', methods=['GET', 'POST'])
def charge(id):
    amount = session.get('amount')
    stripe_amount = amount * 100
    project = Project.query.get_or_404(id)
    customer = stripe.Customer.create(
        email= current_user.email,
        card=request.form['stripeToken']
    )
 
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=stripe_amount,
        currency='usd',
        description= 'IF' + project.who + project.what
    )
    u = current_user._get_current_object()
    p = Project.query.get(id)
    u.projects.append(p)
    db.session.add(u)
    
    project.sum_total_ammount(amount)

    return render_template('charge.html')

@main.route('/chellenge/<int:id>/donate/login', methods=['GET', 'POST'])
def donate_login_required(id):   
    form = LoginForm()
    url_register = url_for('main.register_before_donate', id=id)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.donate', id=id))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form, url_register=url_register)

@main.route('/chellenge/<int:id>/donate/register', methods=['GET', 'POST'])
def register_before_donate(id):   
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@main.route('/')
def index():
    projects = Project.query.filter_by(approved=True).order_by(Project.timestamp.desc()).all()
    today = datetime.now()
    return render_template('index.html', projects=projects, today=today)

@main.route('/current-projects')
def current_projects():
    projects = Project.query.filter_by(approved=True, category=1).order_by(Project.timestamp.desc()).all()
    today = datetime.now()
    return render_template('current_projects.html', projects=projects, today=today)

@main.route('/hall-of-glory')
def hall_of_glory():
    projects = Project.query.filter_by(approved=True, category=2).order_by(Project.timestamp.desc()).all()
    today = datetime.now()
    return render_template('hall_of_glory.html', projects=projects, today=today)

@main.route('/pit-of-shame')
def pit_of_shame():
    projects = Project.query.filter_by(approved=True, category=3).order_by(Project.timestamp.desc()).all()
    today = datetime.now()
    return render_template('pit_of_shame.html', projects=projects, today=today)



@main.route('/create', methods=['GET', 'POST'])
def create():
    form = NewProjectForm1()
    if form.validate_on_submit():
        session['who'] = form.who.data,
        session['what'] = form.what.data,
        session['couse'] = form.couse.data,
        session['background_color'] = form.background_color.data,
        session['emoji1'] = form.emoji1.data
        session['emoji2'] = form.emoji2.data
        session['emoji3'] = form.emoji4.data
        session['emoji4'] = form.emoji3.data
        session['emoji5'] = form.emoji5.data
        return redirect(url_for('main.create_step_2')) 
    return render_template('create.html', form=form) 

@main.route('/create/step_2', methods=['GET', 'POST'])
def create_step_2():
    form = NewProjectForm2()
    who = make_response(session['who'])
    what = make_response(session['what'])
    couse = make_response(session['couse'])
    background_color = make_response(session['background_color'])
    emoji1 = session.get('emoji1')
    emoji2 = session.get('emoji2')
    emoji3 = session.get('emoji3')
    emoji4 = session.get('emoji4')
    emoji5 = session.get('emoji5')
    if form.validate_on_submit():
        project = Project(who=who.data,
                        what=what.data,
                        couse=couse.data,
                        organization_url=form.organization_website.data,
                        background_color=background_color.data,
                        emoji1= emoji1,
                        emoji2=emoji2,
                        emoji3=emoji3,
                        emoji4=emoji4,
                        emoji5=emoji5,
                        about=form.why.data,
                        author=current_user._get_current_object())
        db.session.add(project)
        db.session.commit()
        flash('Thanks, you will ricive a mail when your prject be approved.')
        return redirect(url_for('main.index')) 
    return render_template('create_step2.html', form_step_2=form, who=who.data, what=what.data, couse=couse.data, background_color=background_color.data)

@main.route('/chellenge/<int:id>', methods=['GET', 'POST'])
def challenge(id):
    project = Project.query.get_or_404(id)
    project.sum_viewers_counter()
    form2 = AmountForm()
    if form2.validate_on_submit():
        amount = form2.amount_hidden.data
        session['amount'] = amount
        return redirect(url_for('main.donate', id=id))
    return render_template('challenge.html', projects=[project], project=project, form2=form2)

@main.route('/chellenge/admin/<int:id>', methods=['GET', 'POST'])
def edit_challenge(id):
    project = Project.query.get(id)
    form = EditProjectAdminForm(project=project)
    if form.validate_on_submit():
        project.who = form.who.data
        project.what = form.what.data
        project.couse = form.couse.data
        organization_url = form.organization_url.data
        project.about = form.about.data     
        project.approved = form.approved.data
        project.category = form.category.data
        db.session.add(project)
        flash('The profile has been updated.')
        return redirect(url_for('main.index')) 
    form.who.data = project.who
    form.what.data = project.what
    form.couse.data = project.couse
    form.organization_url.data = project.organization_url
    form.about.data = project.about
    form.category.data = project.category
    form.approved.data = project.approved
    return render_template('edit_challange.html', projects=[project], project=project, form=form)


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
        user.facebook_id = form.facebook_id.data
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
    form.facebook_id.data = user.facebook_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/admin/approve', methods=['GET', 'POST'])
@admin_required
def admin_approve():
    projects = Project.query.order_by(Project.timestamp.desc()).all()
    today = datetime.now()
    return render_template('admin/approve.html', projects=projects, today=today)
