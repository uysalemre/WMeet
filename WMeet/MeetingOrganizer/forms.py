from django import forms
from .models import ContactModel,EventsModel,EventAttendeeModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm,SetPasswordForm,PasswordChangeForm
from django.contrib.admin import widgets
import datetime
from captcha.fields import ReCaptchaField

class ContactForm(forms.ModelForm):
	
	class Meta:
		model = ContactModel
		fields = ['name','email','message']
		
	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Send Message',css_class='main-btn'))
		
		for field in self.fields.values():
			field.widget.attrs['placeholder'] = field.label

class SignupForm(UserCreationForm):
	
	class Meta:
		model = User
		fields = ['username','email','first_name','last_name','password1','password2']
	
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Sign Up', css_class='main-btn'))
		self.fields['email'].required = True
		self.fields['email'].help_text = "Required. Must be confirmed after submission"
		for field in self.fields.values():
			field.widget.attrs['placeholder'] = field.label

class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Login To Application', css_class='main-btn'))
		
class ResetPasswordForm(PasswordResetForm):
	def __init__(self, *args, **kwargs):
		super(ResetPasswordForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Send Email', css_class='main-btn'))
		
class PasswordResetConfirmForm(SetPasswordForm):
	def __init__(self, *args, **kwargs):
		super(PasswordResetConfirmForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Confirm', css_class='main-btn'))
		
class EventCreationForm(forms.ModelForm):
	"""CHOICES = (
		('file', 'FILE'),
		('manual', 'MANUAL'),
	)
	add_method = forms.ChoiceField(choices=CHOICES)"""

	class Meta:
		model = EventsModel
		fields = ['eventname','event_start_date','event_start_time','place','link_end_date','link_end_time']
		widgets = {
			'event_start_date':widgets.AdminDateWidget(attrs={'placeholder':'year-month-day'}),
			'event_start_time': widgets.AdminTimeWidget(attrs={'placeholder': 'hour:minute:second'}),
			'link_end_date': widgets.AdminDateWidget(attrs={'placeholder': 'year-month-day'}),
			'link_end_time': widgets.AdminTimeWidget(attrs={'placeholder': 'hour:minute:second'}),
		}
		
	def __init__(self, *args, **kwargs):
		super(EventCreationForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Create Event', css_class='main-btn'))
		self.fields['place'].label = "Address"
		#self.fields['add_method'].label = "Attendee Addition Method"
		
	
class AttendeeAddForm(forms.ModelForm):
	class Meta:
		model = EventAttendeeModel
		fields = ['name','email','facebook_address']
		
	def __init__(self, *args, **kwargs):
		super(AttendeeAddForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save and Add Another', css_class='main-btn'))

class ChangePasswordForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Change Password', css_class='main-btn'))


"""
class AttendeeAddFileForm(forms.ModelForm):
	class Meta:
		model = FileAttendeeModel
		fields = ['excel_file']
	
	def __init__(self, *args, **kwargs):
		super(AttendeeAddFileForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Add This File', css_class='main-btn'))
		
"""
