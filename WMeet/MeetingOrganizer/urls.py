from django.urls import path
from .views import HomeView
from django.conf.urls import url

app_name = "MeetingOrganizer"

urlpatterns = [
    path('', HomeView.as_view(), name="home")
]