from django.shortcuts import render,redirect,reverse
from django.urls import reverse_lazy
from django.views import generic
from .forms import ContactForm,SignupForm,EventCreationForm,AttendeeAddForm
from django.contrib import messages
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EventAttendeeModel,EventsModel
from .general_queries import general_query
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import datetime


class HomeView(generic.FormView):
	template_name = "index.html"
	form_class = ContactForm
	success_url = reverse_lazy('MeetingOrganizer:home')
	
	def get(self,request,*args, **kwargs):
		if request.user.is_authenticated:
			return redirect('MeetingOrganizer:events')
		return render(request,self.template_name,{'form':self.form_class})
	
	def form_valid(self, form):
		contact = ContactForm(self.request.POST)
		contact.save()
		messages.success(self.request, 'Thanks for message. We will contact you ASAP.')
		return super(HomeView,self).form_valid(form)
	
	def form_invalid(self, form):
		messages.error(self.request,'Form is not submitted. Check your informations again. ')
		return super(HomeView,self).form_invalid(form)
	
class SignupView(generic.FormView):
	template_name = "signup.html"
	form_class = SignupForm
	success_url = reverse_lazy('MeetingOrganizer:home')
	
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('MeetingOrganizer:events')
		return render(request,self.template_name,{'form':self.form_class})
	
	def form_valid(self, form):
		signup = SignupForm(self.request.POST)
		user = signup.save(commit=False)
		user.is_active = False
		user.save()
		message = render_to_string('account_activation_email.html', {
			'user': user,
			'domain': get_current_site(self.request).domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_activation_token.make_token(user),
		})
		user.email_user("Account Activation Email",message)
		messages.success(self.request, 'We an activation link sended your email address. '
									   'Activate your account then you can login. Link will expire in 1 day.')
		return super().form_valid(form)
	
	def form_invalid(self, form):
		messages.error(self.request,'Something went wrong. Check the form try it again.')
		return super().form_invalid(form)

class AccountActivationView(generic.View):

	def get(self,request,uidb64,token):
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.save()
			messages.success(self.request, 'Your activation successfully completed you can login now.')
			return redirect('MeetingOrganizer:login')
		else:
			message = render_to_string('account_activation_email.html', {
				'user': user,
				'domain': get_current_site(self.request).domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.email_user("Account Activation Email", message)
			messages.success(self.request, 'Your activation was expired. So we sended another one to your Email. Go and check it !')
			return redirect('MeetingOrganizer:home')

class EventsView(LoginRequiredMixin, generic.View):
	login_url = '/login/'
	redirect_field_name = 'login'
	template_name = "events.html"
	
	def get(self, request):
		myevents = EventsModel.objects.all().filter(creator=request.user)
		return render(request, self.template_name, {'events': myevents,'domain':get_current_site(request).domain})

class CreateEventView(LoginRequiredMixin,generic.FormView):
	login_url = '/login/'
	redirect_field_name = 'login'
	template_name = "eventcreate.html"
	form_class = EventCreationForm
	event_name = None
	pk = None
	
	def get_success_url(self):
		return reverse('MeetingOrganizer:add_attendee', kwargs={'pk': self.pk.pk,'event_name':self.event_name})
	
	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{'form':self.form_class})
	
	def form_valid(self, form):
		if form.cleaned_data['event_start_date'] < datetime.date.today():
			form.add_error(None,"The event start date cannot be in the past!")
			return self.form_invalid(form)
		if (form.cleaned_data['link_end_date'] < datetime.date.today()) or not (datetime.datetime.combine(form.cleaned_data['link_end_date'],form.cleaned_data['link_end_time']) < datetime.datetime.combine(form.cleaned_data['event_start_date'],form.cleaned_data['event_start_time'])) :
			form.add_error(None,"The link end date must expire before the event start date, also it must not be before today !")
			return self.form_invalid(form)
		else:
			newevent = EventsModel(eventname=form.cleaned_data['eventname'],
								   event_start_date=form.cleaned_data['event_start_date'],
								   event_start_time=form.cleaned_data['event_start_time'],
								   place=form.cleaned_data['place'],
								   link_end_date=form.cleaned_data['link_end_date'],
								   link_end_time=form.cleaned_data['link_end_time'],
								   creator=self.request.user)
			newevent.save()
			self.event_name = form.cleaned_data['eventname']
			self.pk = general_query.eventcheck(self.request.user,newevent.eventname,newevent.pk)
			messages.success(self.request, 'Event creation completed. Now you can add your attendees')
			return super().form_valid(form)
	
	def form_invalid(self, form):
		return super().form_invalid(form)

class AddAttendeeView(LoginRequiredMixin,generic.FormView):
	login_url = '/login/'
	redirect_field_name = 'login'
	template_name = "attendeeadd.html"
	form_class = AttendeeAddForm
	
	def get_success_url(self):
		return reverse_lazy('MeetingOrganizer:add_attendee', kwargs={'pk': self.kwargs['pk'],'event_name':self.kwargs['event_name']})
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['event_name'] = self.kwargs['event_name']
		return context
	
	def get(self, request,*args, **kwargs):
		if general_query.eventcheck(request.user,kwargs['event_name'],kwargs['pk']):
			return render(request, self.template_name, {'form': self.form_class, 'pk':self.kwargs['pk'],
														'event_name':self.kwargs['event_name']})
		else:
			return redirect('MeetingOrganizer:events')
	
	def form_valid(self, form):
		event = general_query.eventcheck(self.request.user,self.kwargs['event_name'],self.kwargs['pk'])
		attendee = EventAttendeeModel.objects.all().filter(event=event,email=form.cleaned_data['email']).first()
		if attendee:
			form.add_error(None,"This attendee already given")
			return self.form_invalid(form)
		add = EventAttendeeModel(name=form.cleaned_data['name'],
								 email=form.cleaned_data['email'],
								 facebook_address=form.cleaned_data['facebook_address'],
								 event = event)
		add.save()
		messages.success(self.request,"Attendee added")
		return super(AddAttendeeView, self).form_valid(form)
	
	def form_invalid(self, form):
		return super(AddAttendeeView,self).form_invalid(form)
	
"""class AddAttendeeFileView(LoginRequiredMixin,generic.FormView):
	login_url = '/login/'
	redirect_field_name = 'login'
	template_name = "attendeeaddfile.html"
	form_class = AttendeeAddFileForm
	
	def get_success_url(self):
		return reverse('MeetingOrganizer:summary', kwargs={'pk': self.kwargs['pk'],'event_name':self.kwargs['event_name']})
	
	def get(self, request, *args, **kwargs):
		if general_query.eventcheck(request.user,kwargs['event_name'],kwargs['pk']):
			return render(request,self.template_name,{'form':self.form_class})
		else:
			return redirect('MeetingOrganizer:events')
	
	def form_valid(self, form):
		fileadd =FileAttendeeModel(event = general_query.eventcheck(self.request.user,
																	self.kwargs['event_name'],
																	self.kwargs['pk']),
								   excel_file=form.cleaned_data['excel_file'])
		fileadd.save()
		messages.success(self.request,"Excel file added successfully to our system")
		return super().form_valid(form)
	
	
	def form_invalid(self, form):
		return super().form_invalid(form)"""
	
class EventSummaryView(LoginRequiredMixin,generic.View):
	login_url = '/login/'
	redirect_field_name = 'login'
	template_name = "eventsummary.html"
	
	def get(self,request,event_name,pk):
		event = general_query.eventcheck(request.user,event_name,pk)
		if event:
			attendees = general_query.getattendees(event)
			if attendees:
				participatornumber = attendees.filter(is_participating = True).count()
				return render(request,self.template_name,{'event':event,'attendees':attendees,'numofparticipator':participatornumber})
			else:
				messages.error(request,"Please first add attendee to see summary")
				return redirect('MeetingOrganizer:add_attendee', event_name=event_name,pk=pk)
		else:
			return redirect('MeetingOrganizer:events')
		
class AttendeeAttendanceView(generic.View):
	
	def get(self,request,event_pk,event_name,user_pk,yesorno):
		try:
			eventpk = force_text(urlsafe_base64_decode(event_pk))
			eventname = force_text(urlsafe_base64_decode(event_name))
			attendeepk = force_text(urlsafe_base64_decode(user_pk))
			yesno = force_text(urlsafe_base64_decode(yesorno))
			event = EventsModel.objects.all().filter(pk=eventpk, eventname=eventname).first()
			attendee = EventAttendeeModel.objects.all().filter(pk=attendeepk).first()
		except (TypeError, ValueError, OverflowError):
			event = None
			attendee = None
		if attendee is not None and event is not None:
			print(datetime.datetime.combine(event.link_end_date,event.link_end_time), datetime.datetime.now())
			if datetime.datetime.combine(event.link_end_date,event.link_end_time) < datetime.datetime.combine(event.event_start_date,event.event_start_time):
				attendee.is_participating = True if yesno == "yes" else False
				attendee.save()
				messages.success(request,"Your participation status changed. Thanks.")
			else:
				messages.error(request,"Link is expired and you passed the allowed time for giving answer about your status.")
			return redirect('MeetingOrganizer:home')
		else:
			messages.error(request,"You are not authorized to access this page.")
			return redirect('MeetingOrganizer:home')
			
class SendNotificationsToUsersView(LoginRequiredMixin,generic.View):
	login_url = '/login/'
	redirect_field_name = 'login'
	
	def get(self,request,event_name,pk):
		event = general_query.eventcheck(request.user, event_name, pk)
		if event:
			general_query.sendlinks(request,event)
			messages.success(request,"Your notifications sended successfully.")
			return redirect('MeetingOrganizer:events')
		else:
			return redirect('MeetingOrganizer:events')
		
	

	