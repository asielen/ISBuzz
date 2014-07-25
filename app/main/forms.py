from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Length, Email
from wtforms import ValidationError
from ..models import Role, User, Region


class EditProfileForm(Form):
    region = StringField('Region', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.region.choices = [(region.id, region.name)
                             for region in Region.query.order_by(Region.name).all()]
        self.user = user


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    region = StringField('Region', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.region.choices = [(region.id, region.name)
                             for region in Region.query.order_by(Region.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
