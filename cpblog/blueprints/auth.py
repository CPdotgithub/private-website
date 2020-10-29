from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
import os
from cpblog.settings import Operations
from cpblog.emails import send_confirm_email,send_reset_password_email
from cpblog.extensions import db
from cpblog.forms.auth import LoginForm,RegisterForm,ForgetPasswordForm, ResetPasswordForm
from cpblog.utils import generate_token, validate_token, redirect_back
from cpblog.models import Admin

auth_bp = Blueprint('auth',__name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data.lower()).first()
        if admin is not None and admin.validate_password(form.password.data):
            if login_user(admin, form.remember_me.data):
                flash('Login success.', 'info')
                return redirect(url_for('blog.index'))
            else:
                flash('Your account is blocked.', 'warning')
                return redirect(url_for('blog.index'))
        flash('非法邮箱或密码.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/re-authenticate', methods=['GET', 'POST'])
@login_required
def re_authenticate():
    if login_fresh():
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit() and current_user.validate_password(form.password.data):
        confirm_login()
        return redirect_back()
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('blog.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        InviteCode = form.SecretCode.data
        if InviteCode==os.getenv('SecretCode'):
            admin =Admin(name=name, email=email, username=username)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            token = generate_token(admin=admin, operation='confirm')
            send_confirm_email(admin=admin, token=token)
            flash('确认邮件已发送，请检查邮箱.', 'info')
            return redirect(url_for('.login'))
        else:
            flash("邀请码错误" ,'info')
    return render_template('auth/register.html', form=form)


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('blog.index'))

    if validate_token(admin=current_user, token=token, operation='confirm'):
        print(token)
        flash('账户确认.', 'success')
        
        return redirect(url_for('blog.index'))
    else:
        flash('非法或失效token.', 'danger')
        return redirect(url_for('.resend_confirm_email'))


@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        return redirect(url_for('blog.index'))

    token = generate_token(admin=current_user, operation=Operations.CONFIRM)
    send_confirm_email(admin=current_user, token=token)
    flash('新邮箱已设置，请检查邮箱', 'info')
    return redirect(url_for('blog.index'))


@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = ForgetPasswordForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data.lower()).first()
        if admin:
            token = generate_token(admin=admin, operation=Operations.RESET_PASSWORD)
            send_reset_password_email(admin=admin, token=token)
            flash('改密邮件已发送，请检查邮箱.', 'info')
            return redirect(url_for('.login'))
        flash('非法邮箱地址.', 'warning')
        return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data.lower()).first()
        if admin is None:
            return redirect(url_for('blog.index'))
        if validate_token(admin=admin, token=token, operation=Operations.RESET_PASSWORD,new_password=form.password.data):
            flash('密码更新.', 'success')
            return redirect(url_for('.login'))
        else:
            flash('非法或失效连接.', 'danger')
            return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)