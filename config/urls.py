from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from formLegend.views import DashboardView, AddWebsiteView, EditWebsiteView, \
    DeleteWebsiteView, AddFormView, ViewFormView, EditFormView, DeleteFormView

from registration.views import activate
from registration.views import register

from captchaForm import *

import forms_builder.forms.urls  # remove when done with it

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #admin and grappelli skin for admin urls
    url(r'^admin/', include(admin.site.urls)),
    url(r'^formBuilder/', include(forms_builder.forms.urls)),  # remove when done with it
    url(r'^grappelli/', include('grappelli.urls')),
    #django-simple-captcha
    url(r'^captcha/', include('captcha.urls')),
    #may need this for favicon.ico but I am not sure
    #url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
)

#url patterns for django-registration
urlpatterns += patterns('',
   url(r'^activate/complete/$',
       TemplateView.as_view(template_name='registration/activation_complete.html'),
       name='registration_activation_complete'),
   # Activation keys get matched by \w+ instead of the more specific
   # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
   # that way it can return a sensible "invalid key" message instead of a
   # confusing 404.
   url(r'^activate/(?P<activation_key>\w+)/$',
       activate,
       {'backend': 'registration.backends.default.DefaultBackend',
       'extra_context': {'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS}},
       name='registration_activate'),
   url(r'^register/$',
       register,
       {'form_class': CaptchaRegistrationForm, 'backend': 'registration.backends.default.DefaultBackend'},
       name='registration_register'),
   url(r'^register/complete/$',
       TemplateView.as_view(template_name='registration/registration_complete.html'),
       name='registration_complete'),
   url(r'^register/closed/$',
       TemplateView.as_view(template_name='registration/registration_closed.html'),
       name='registration_disallowed'),
   #django-registration auth urls
   url(r'^login/$',
       auth_views.login,
       {'template_name': 'registration/login.html'},
       name='auth_login'),
   url(r'^logout/$',
       auth_views.logout,
       {'template_name': 'formLegend/home.html'},
       name='auth_logout'),
   url(r'^password/change/$',
       auth_views.password_change,
       name='auth_password_change'),
   url(r'^password/change/done/$',
       auth_views.password_change_done,
       name='auth_password_change_done'),
   url(r'^password/reset/$',
       auth_views.password_reset,
       name='auth_password_reset'),
   url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       name='auth_password_reset_confirm'),
   url(r'^password/reset/complete/$',
       auth_views.password_reset_complete,
       name='auth_password_reset_complete'),
   url(r'^password/reset/done/$',
       auth_views.password_reset_done,
       name='auth_password_reset_done'),
)

#url patterns for formLegend
urlpatterns += patterns('',
    url(r'^$', TemplateView.as_view(template_name='formLegend/home.html'), name='home'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^websites/add/$', AddWebsiteView.as_view(), name='add_fl_website'),
    url(r'^websites/edit/(?P<slug>[-\w]+)/$', EditWebsiteView.as_view(), name='edit_fl_website'),
    url(r'^websites/delete/(?P<slug>[-\w]+)/$', DeleteWebsiteView.as_view(), name='delete_fl_website'),
    url(r'^forms/add/$', AddFormView.as_view(), name='add_fl_form'),
    url(r'^forms/view/(?P<slug>[-\w]+)/$', ViewFormView.as_view(), name='view_fl_form'),
    url(r'^forms/edit/(?P<slug>[-\w]+)/$', EditFormView.as_view(), name='edit_fl_form'),
    url(r'^forms/delete/(?P<slug>[-\w]+)/$', DeleteFormView.as_view(), name='delete_fl_form'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
