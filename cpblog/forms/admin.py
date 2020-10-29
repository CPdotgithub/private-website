
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length,Regexp

from cpblog.forms.user import EditProfileForm
from cpblog.models import Admin


class EditProfileAdminForm(EditProfileForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254),Regexp('.*@.*\.com',message='qq邮箱')])
    
    active = BooleanField('Active')
    confirmed = BooleanField('Confirmed')
    submit = SubmitField()

    def __init__(self, admin, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
        for role in Role.query.order_by(Role.name).all()]
        self.admin = admin

    def validate_username(self, field):
        if field.data != self.admin.username and Admin.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')

    def validate_email(self, field):
        if field.data != self.admin.email and Admin.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('The email is already in use.')

