from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .models import *
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from fbchat import Client
from fbchat.models import *



class GeneralDbQueriesUsed:
	
	def __init__(self):
		self.faceadminemail = ''
		self.faceadminpassword = ''
		self.client = Client(self.faceadminemail, self.faceadminpassword)
	
	def eventcheck(self, creator, event_name, pk):
		return EventsModel.objects.all().filter(creator=creator, eventname=event_name, pk=pk).first()
	
	def getattendees(self,event):
		return EventAttendeeModel.objects.all().filter(event=event)
	
	"""def getfile(self,event):
		return FileAttendeeModel.objects.all().filter(event=event).first()"""

	def sendlinks(self,request,event):
		attendees = general_query.getattendees(event)
		for person in attendees:
			if not self.client.isLoggedIn():
				self.client.login(self.faceadminemail,self.faceadminpassword,max_tries=1)
			if not person.is_link_sended:
				if person.email:
					send_mail(
						subject=event.eventname,
						message=strip_tags(render_to_string("eventinvitation.html",
															{'invitor': request.user.email,
															 'attendee': person.name,
															 'domain': get_current_site(request).domain,
															 'event': event,
															 'event_pk': urlsafe_base64_encode(force_bytes(event.pk)),
															 'user_pk': urlsafe_base64_encode(force_bytes(person.pk)),
															 'statusyes': urlsafe_base64_encode(force_bytes("yes")),
															 'statusno': urlsafe_base64_encode(force_bytes("no")),
															 'event_name':urlsafe_base64_encode(force_bytes(event.eventname)),
															 }
															)
										   ),
						from_email=settings.EMAIL_HOST_USER,
						recipient_list=[person.email],
						html_message=render_to_string("eventinvitation.html",
													  {'invitor': request.user.email,
													   'attendee': person.name,
													   'domain': get_current_site(request).domain,
													   'event': event,
													   'event_pk': urlsafe_base64_encode(force_bytes(event.pk)),
													   'user_pk': urlsafe_base64_encode(force_bytes(person.pk)),
													   'statusyes': urlsafe_base64_encode(force_bytes("yes")),
													   'statusno': urlsafe_base64_encode(force_bytes("no")),
													   'event_name': urlsafe_base64_encode(force_bytes(event.eventname)),
													   }
													  ),
						fail_silently=False,
					)
					person.is_link_sended = True
				if person.facebook_address:
					try:
						if "profile.php?id=" in person.facebook_address:
							user = person.facebook_address.rsplit('profile.php?id=', 1).pop()
							self.client.send(Message(text=strip_tags(render_to_string("eventinvitation.html",
																					  {'invitor': request.user.email,
																					   'attendee': person.name,
																					   'domain': get_current_site(
																						   request).domain,
																					   'event': event,
																					   'event_pk': urlsafe_base64_encode(
																						   force_bytes(event.pk)),
																					   'user_pk': urlsafe_base64_encode(
																						   force_bytes(person.pk)),
																					   'statusyes': urlsafe_base64_encode(
																						   force_bytes("yes")),
																					   'statusno': urlsafe_base64_encode(
																						   force_bytes("no")),
																					   'event_name': urlsafe_base64_encode(
																						   force_bytes(
																							   event.eventname)),
																					   }
																					  )
																	 )), thread_id=user,
											 thread_type=ThreadType.USER)
							print("me too")
							person.is_link_sended = True
						else:
							userid = person.facebook_address.rsplit('/', 1).pop()
							users = self.client.searchForUsers(userid)
							print(users)
							user = users[0]
							print("User's ID: {}".format(user.uid))
							print("User's name: {}".format(user.name))
							print("User's profile picture URL: {}".format(user.photo))
							print("User's main URL: {}".format(user.url))
							self.client.send(Message(text=strip_tags(render_to_string("eventinvitation.html",
																	{'invitor': request.user.email,
																	 'attendee': person.name,
																	 'domain': get_current_site(request).domain,
																	 'event': event,
																	 'event_pk': urlsafe_base64_encode(force_bytes(event.pk)),
																	 'user_pk': urlsafe_base64_encode(force_bytes(person.pk)),
																	 'statusyes': urlsafe_base64_encode(force_bytes("yes")),
																	 'statusno': urlsafe_base64_encode(force_bytes("no")),
																	 'event_name':urlsafe_base64_encode(force_bytes(event.eventname)),
																	 }
																	)
												   )),thread_id=user.uid,thread_type=ThreadType.USER)
						person.is_link_sended = True
					except:
						pass
				person.save()
			
general_query = GeneralDbQueriesUsed()