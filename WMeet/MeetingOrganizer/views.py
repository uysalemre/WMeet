from django.shortcuts import render
from django.views import generic
from .forms import ContactForm
from django.contrib import messages
from .models import ContactModel
import json
# Create your views here.

class HomeView(generic.FormView):
	template_name = "index.html"
	form_class = ContactForm
	success_url = '/'
	
	def get(self,request,*args, **kwargs):
		return render(request,self.template_name,{'form':self.form_class})
	
	def form_valid(self, form):
		data = ContactModel(name=form.cleaned_data['name'],email=form.cleaned_data['email'],message=form.cleaned_data['message'])
		data.save()
		messages.success(self.request, 'Thanks for message. We will contact you ASAP.')
		return super().form_valid(form)
	
	def form_invalid(self, form):
		messages.error(self.request,'Error happened when submitting your form try it again.')
		return super().form_invalid(form)
	
	