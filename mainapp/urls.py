from django.urls import path,include
from . import views
from django.contrib import admin
from django.urls import path,include
from mainapp import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from mainapp.forms import (PwdResetConfirmForm, PwdResetForm)

app_name = 'mainapp'

urlpatterns = [
    path('',views.index),
    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.signup,name='signup'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate,name='activate'),
    #reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="mainapp/user/password_reset_form.html",
                                                                 success_url='password_reset_email_confirm',
                                                                 email_template_name='mainapp/user/password_reset_email.html',
                                                                 form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='mainapp/user/password_reset_confirm.html',
                                                                                                success_url='/password_reset_complete', 
                                                                                                form_class=PwdResetConfirmForm),
         name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="mainapp/user/reset_status.html"), name='password_reset_done'),
    path('password_reset_complete/',
         TemplateView.as_view(template_name="mainapp/user/reset_status.html"), name='password_reset_complete'),
    path('delete_user/',views.delete_user, name='delete_user'),
    path('delete_confirmation/',views.delete_confirmation,name='delete_confirmation'),
    path('delete_cancel/',views.delete_cancel,name='delete_cancel'),
    path('account/', views.account, name='account'),
    path('account_update/', views.account_update, name='account_update'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/registration',views.registration,name='registration'),
    path('contact/', views.contact,name='contact'),
    path('privacy/', views.privacy,name='privacy'),
    path('calendar/',views.CalendarView.as_view(),name='calendar'),
    path('calendar/<int:year>/<int:month>/<int:day>',views.CalendarView.as_view(),name='calendar'),
    path('booking/<int:year>/<int:month>/<int:day>/<int:hour>',views.BookingView.as_view(),name='booking'),
    path('schedule/<int:year>/<int:month>/<int:day>/',views.ScheduleView.as_view(),name='schedule'),
    path('schedule/holiday/<int:year>/<int:month>/<int:day>/<int:hour>',views.holiday,name='holiday'),
    path('schedule/delete/<int:year>/<int:month>/<int:day>/<int:hour>',views.delete,name='delete'),
    path('schedule/user/',views.user_schedule,name='user_schedule'),
    path('schedule/user/delete/<int:pk>',views.user_schedule_delete,name='user_schedule_delete'),
   

]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
