#-*- coding:UTF-8 -*-
from flask_wtf import Form
from wtforms import SelectField, StringField, TextAreaField, \
    SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class CommonForm(Form):
    types = SelectField(u'分类', coerce=int, validators=[DataRequired()])
    source = SelectField(u'来源', coerce=int, validators=[DataRequired()])


class SignInForm(Form):
    username = StringField(u'用户名',
                           validators=[DataRequired()])
    email = SelectField(u'电子邮件',
                        validators=[DataRequired(), Length(1, 64), Email()])
    password1 = PasswordField(u'密码',
                              validators=[DataRequired(),
                                          EqualTo('password2', message=u'两次密码不一致!')])
    password2 = PasswordField(u'确认密码',
                              validators=[DataRequired()])


class ChangePwdForm(Form):
    old_password = PasswordField(u'旧密码',
                                 validators=[DataRequired()])
    new_password = PasswordField(u'新密码',
                                 validators=[DataRequired(),
                                             EqualTo('new_password2', message=u'两次密码不一致!')])
    new_password2 = PasswordField(u'确认新密码',
                                  validators=[DataRequired()])
