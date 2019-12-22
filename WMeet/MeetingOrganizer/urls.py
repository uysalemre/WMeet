from django.urls import path,reverse_lazy,reverse
from .views import HomeView, SignupView, AccountActivationView, EventsView, CreateEventView,\
    AddAttendeeView,EventSummaryView,AttendeeAttendanceView,SendNotificationsToUsersView
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm,ResetPasswordForm, PasswordResetConfirmForm,ChangePasswordForm



app_name = "MeetingOrganizer"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('events/', EventsView.as_view(), name="events"),
    path('create-event/',CreateEventView.as_view(),name="create_event"),
    path('create-event/add-attendee/<str:event_name>/<int:pk>',AddAttendeeView.as_view(),name="add_attendee"),
    #path('create-event/add-attendee/file/<str:event_name>/<int:pk>',AddAttendeeFileView.as_view(),name="add_attendee_file"),
    path('create-event/add-attendee/<str:event_name>/<int:pk>/summary',EventSummaryView.as_view(),name="summary"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',AccountActivationView.as_view(), name='activate'),
    url(r'event-attendance/(?P<event_pk>[0-9A-Za-z_\-]+)/(?P<event_name>[0-9A-Za-z_\-]+)/(?P<user_pk>[0-9A-Za-z_\-]+)/(?P<yesorno>[0-9A-Za-z_\-]+)/$',AttendeeAttendanceView.as_view(),name='attendance'),
    path('send-notifications/<str:event_name>/<int:pk>/',SendNotificationsToUsersView.as_view(),name='sendnotifications'),
    path('login/',auth_views.LoginView.as_view(template_name = 'registration/login.html',
                                               authentication_form=UserLoginForm,
                                               redirect_authenticated_user=True),
                                               name = "login"),
    path('logout/',auth_views.LogoutView.as_view(), name="logout"),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html',
                                                                 form_class =ResetPasswordForm,
                                                                 email_template_name = 'registration/password_reset_email.html',
                                                                 success_url = reverse_lazy('MeetingOrganizer:password_reset_done')),
                                                                 name="password_reset"),
    path('reset-password/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
                                                  name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm.html',
                                                                               form_class = PasswordResetConfirmForm,
                                                                               success_url = reverse_lazy('MeetingOrganizer:password_reset_complete')),
                                                                                name = 'password_reset_confirm'),
    path('reset/done/ ',auth_views.PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_complete.html'),name='password_reset_complete'),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='profile/change_password.html',
                                                                 form_class = ChangePasswordForm,
                                                                 success_url=reverse_lazy('MeetingOrganizer:events'),
                                                                 ),name="change_password"),
]