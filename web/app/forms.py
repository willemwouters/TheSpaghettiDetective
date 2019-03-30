from django.db import models
from django.forms import ModelForm, Form, CharField, ChoiceField
import phonenumbers

from .widgets import CustomRadioSelectWidget, PhoneCountryCodeWidget
from .models import *

class PrinterForm(ModelForm):
    class Meta:
        model = Printer
        fields = ['name', 'action_on_failure', 'tools_off_on_pause', 'bed_off_on_pause', 'detective_sensitivity', 'retract_on_pause', 'lift_z_on_pause']
        widgets = {
            'action_on_failure': CustomRadioSelectWidget(choices=Printer.ACTION_ON_FAILURE),
        }

class UserPrefernecesForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

### Phone verification ##

class PhoneVerificationForm(Form):
    phone_country_code = CharField(max_length=5, widget=PhoneCountryCodeWidget())
    phone_number = CharField(max_length=12)
    via = ChoiceField(
        choices=[('sms', 'Text me (SMS)'), ('call', 'Call me')],
        widget=CustomRadioSelectWidget())

    def clean_phone_country_code(self):
        phone_country_code = self.cleaned_data['phone_country_code']
        if not phone_country_code.startswith('+'):
            phone_country_code = '+' + phone_country_code
        return phone_country_code

    def clean(self):
        data = self.cleaned_data
        phone_number = data['phone_country_code'] + data['phone_number']
        try:
            phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number):
                self.add_error('phone_number', 'Invalid phone number')
        except phonenumbers.NumberParseException as e:
            self.add_error('phone_number', e)

class PhoneTokenForm(Form):
    token = CharField(max_length=6)
