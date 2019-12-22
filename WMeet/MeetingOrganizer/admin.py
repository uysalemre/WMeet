from django.contrib import admin
from .models import ContactModel,EventsModel,EventAttendeeModel

# Register your models here.

admin.site.register(ContactModel)
admin.site.register(EventsModel)
admin.site.register(EventAttendeeModel)
"""admin.site.register(FileAttendeeModel)"""

