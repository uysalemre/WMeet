from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import FileExtensionValidator
from django.core.files.storage import FileSystemStorage
from django.conf.global_settings import MEDIA_ROOT


fs = FileSystemStorage(location=MEDIA_ROOT+'MeetingOrganizer/eventcontacts/')

class ContactModel(models.Model):
	name = models.CharField(max_length=120,null=False,blank=False)
	email = models.EmailField(null=False,blank=False)
	message = models.TextField(null=False,blank=False)
	User._meta.get_field('email')._unique = True
	
	def __str__(self):
		return self.name
	
class EventsModel(models.Model):
	eventname = models.CharField(max_length=120,null=False)
	event_start_date = models.DateField(null=False,default=datetime.date.today)
	event_start_time = models.TimeField(null=False,default=datetime.datetime.now().strftime("%H:%M:%S"))
	place = models.TextField(null=False,blank=False)
	link_end_date = models.DateField(null=False,default=datetime.date.today)
	link_end_time = models.TimeField(null=False,default=datetime.datetime.now().strftime("%H:%M:%S"))
	creator = models.ForeignKey(User,on_delete=models.PROTECT)
	
	def __str__(self):
		return self.eventname
	
class EventAttendeeModel(models.Model):
	name = models.CharField(max_length=120,null=False)
	email = models.EmailField(null=False,blank=False)
	facebook_address = models.URLField(blank=True)
	is_participating = models.BooleanField(default=False)
	is_link_sended = models.BooleanField(default=False)
	event = models.ForeignKey(EventsModel,on_delete=models.PROTECT)
	
	
	def __str__(self):
		return self.name

"""
class FileAttendeeModel(models.Model):
	event = models.ForeignKey(EventsModel, on_delete=models.PROTECT)
	excel_file = models.FileField(null=False,blank=False,storage=fs,validators=[FileExtensionValidator(allowed_extensions=['xlsx','xls'])])

	def __str__(self):
		return self.excel_file.name
"""