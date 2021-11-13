from django import forms
from django.db.models import fields
from .models import Register
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Row,Column,Layout

class RegisterModelForm(forms.ModelForm):
    class Meta:
        model = Register
        # fields = "__all__"
        # fields = ("name","mobile","email")
        exclude = ['password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.CharField(max_length=25)
    password = forms.CharField(max_length=15)
    mobile = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column('name', css_class='form-group col-md-6 mb-0'),
            Column('email', css_class='form-group col-md-6 mb-0'),
            Column('mobile', css_class='form-group col-md-6 mb-0'),
            Column('password', css_class='form-group col-md-6 mb-0'),
            Submit('submit', 'Submit')
        )