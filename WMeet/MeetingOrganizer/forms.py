from django import forms
from .models import ContactModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from captcha.fields import ReCaptchaField

class ContactForm(forms.ModelForm):
	captcha = ReCaptchaField()
	
	class Meta:
		model = ContactModel
		fields = ['name','email','message']
		required = ['name','email','message']
		
	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Send',css_class='main-btn'))
		
		for field in self.fields.values():
			field.widget.attrs['placeholder'] = field.label
