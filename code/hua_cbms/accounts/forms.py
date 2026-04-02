from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .checks import validate_password


class SignUpForm(forms.Form):

    email = forms.EmailField(label=_('Το email σας') )
    name = forms.CharField(label=_('To μικρό σας όνομα'), max_length = 40)
    surname = forms.CharField(label=_('To επίθετο σας'),max_length = 100)
    password1 = forms.CharField(label=_('Κωδικός πρόσβασης'),max_length = 100, widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password2 = forms.CharField(label=_('Κωδικός πρόσβασης (επανάληψη)'),max_length = 100, widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def __init__(self, *args, **kwargs):
        email = kwargs.pop('email', None)
        super().__init__(*args, **kwargs)
        if email:
           self.fields['email'].disabled = True
           self.fields['email'].initial = email


    def complexity_message(self):
        return _('Παρακαλούμε τηρήστε τις οδηγίες στην οθόνη για τον κωδικό σας!') 
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        email = cleaned_data['email']

        validate_password(password1, password2)
        
        if settings.INTERNAL_DOMAIN in email:
            raise forms.ValidationError( _('Δεν μπορείτε να χρησιμοποιήσετε διεύθυνση ταχυδρομείου @') + settings.INTERNAL_DOMAIN)

        User = get_user_model()
        users = User.objects.filter(email = email)
        if users.count() > 0:
            raise forms.ValidationError(_('Υπάρχει ήδη χρήστης με αυτό το e-mail') )
        
        return cleaned_data
        
class RegisterForm(forms.Form):

    email1 = forms.EmailField(label=_('Το e-mail σας:') )
    email2 = forms.EmailField(label=_('Το e-mail σας (ξανά):') )
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean(self):
        cleaned_data = super().clean()
        if ('email1' not in cleaned_data) or ('email2' not in cleaned_data):
            raise forms.ValidationError( _('Εισάγετε μία έγκυρη διεύθυνση ηλεκτρονικού ταχυδρομείου') )
        
        email1 = cleaned_data['email1']
        email2 = cleaned_data['email2']
        
        if email1 != email2:
            raise forms.ValidationError(_('Τα email πρέπει να ταυτίζονται!') )
        
        if settings.INTERNAL_DOMAIN in email1:
            raise forms.ValidationError( _('Αν έχετε ήδη email της μορφής @') + settings.INTERNAL_DOMAIN + _(' δεν χρειάζεται να εγγραφείτε.') )
        
        User = get_user_model()
        users = User.objects.filter(email = email1)
        if users.count() > 0:
            raise forms.ValidationError( _('Υπάρχει ήδη χρήστης με αυτό το e-mail') )

class ForgotPasswordForm(forms.Form):
    email1 = forms.EmailField(label= _('Το e-mail σας:'))
    email2 = forms.EmailField(label= _('Το e-mail σας (ξανά):'))
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean(self):
        cleaned_data = super().clean()
        if ('email1' not in cleaned_data) or ('email2' not in cleaned_data):
            raise forms.ValidationError(_('Εισάγετε μία έγκυρη διεύθυνση ηλεκτρονικού ταχυδρομείου'))
        
        email1 = cleaned_data['email1']
        email2 = cleaned_data['email2']
        
        if email1 != email2:
            raise forms.ValidationError(_('Τα email πρέπει να ταυτίζονται!'))
        
        if settings.INTERNAL_DOMAIN in email1:
            raise forms.ValidationError(_('Αν έχετε ήδη email της μορφής @') + settings.INTERNAL_DOMAIN + _(' δεν μπορείτε να επαναφέρετε τον κωδικό σας μέσω αυτού του συστήματος.') )
        
        User = get_user_model()
        users = User.objects.filter(email = email1)
        if users.count() == 0:
            raise forms.ValidationError(_('Δεν υπάρχει χρήστης με αυτό το e-mail') )
        
          
class PasswordForm(forms.Form):

    password1 = forms.CharField(label=_('Νέος κωδικός πρόσβασης'),max_length = 100, widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password2 = forms.CharField(label=_('Νέος κωδικός πρόσβασης (επανάληψη)'),max_length = 100, widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        validate_password(password1, password2)

