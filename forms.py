from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

# Kullanıcı Kayıt Formu
class RegistrationForm(FlaskForm):
    kullanici_adi = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=25)])
    sifre = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    sifre_tekrar = PasswordField('Şifre Tekrar', validators=[DataRequired(), EqualTo('sifre', message="Şifreler eşleşmeli")])
    submit = SubmitField('Kayıt Ol')

# Kullanıcı Giriş Formu
class LoginForm(FlaskForm):
    kullanici_adi = StringField('Kullanıcı Adı', validators=[DataRequired()])
    sifre = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')

# Kitap Ekleme Formu
class KitapForm(FlaskForm):
    kitap_adi = StringField('Kitap Adı', validators=[DataRequired()])
    yazar = StringField('Yazar', validators=[DataRequired()])
    submit = SubmitField('Kitap Ekle')
