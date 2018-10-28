from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, ContactForm
from app.models import User, Contact
from app.main import bp
import sys


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ContactForm()
    if form.validate_on_submit():
        # print (request.form)
        # print(form, file=sys.stderr)
        contact = Contact(name=form.name.data, phone_no=form.phone_no.data, email=form.email.data, user_id=current_user.id)
        db.session.add(contact)
        db.session.commit()
        flash(_('Contact added sucessfully!'))
        return redirect(url_for('main.index'))
    return render_template('index.html', title=_('Home'), form=form)

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    contacts = Contact.query.order_by(Contact.timestamp.desc()).paginate(
        page, current_app.config['CONTACTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=contacts.next_num) \
        if contacts.has_next else None
    prev_url = url_for('main.explore', page=contacts.prev_num) \
        if contacts.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           contacts=contacts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


