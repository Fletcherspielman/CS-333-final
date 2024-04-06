from django.urls import path, include
from main_page import views as main
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
app_name = "login"
# https://studygyaan.com/django/how-to-create-built-in-change-password-and-reset-password-in-django
# the reset password is a more complicated system sense were using djangos reset password system 
# it will use the urls from the auth system in django and use are own templates to display it 
# there will be little to no back end code that is written by us
# thanks to Huzaif Sayyed for doing the research and showing us how to do it
urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('good_login', views.good_login , name="good_login"),
    path('logout_user', views.logout_user , name="logout_user"),
    path('', include('main_page.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='lost_password/password_reset_form.html',
        html_email_template_name='lost_password/email_template.html',
        email_template_name='lost_password/email_template.html',
        subject_template_name='lost_password/subject.txt',
        success_url='/password_reset_done/'
    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='lost_password/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='lost_password/password_reset_confirm.html',
        success_url='/password_reset_complete/'
    ), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='lost_password/password_reset_complete.html'
    ), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 