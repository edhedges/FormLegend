from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.simple import direct_to_template

from django.contrib.auth import views as auth_views

from registration.views import activate
from registration.views import register

from captchaForm import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'home.html'}, name='home'),
    #admin and grappelli skin for admin urls
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    #django-registration
    #url(r'^accounts/', include('registration.urls')),

    #django-simple-captcha
    url(r'^captcha/', include('captcha.urls')),

    #may need this for favicon.ico but I am not sure
    #url(r'^favicon\.ico$', RedirectView.as_view(url='/static/project/img/favicon.ico')),
)

#url patterns for django-registration
urlpatterns += patterns('',
   url(r'^activate/complete/$',
       direct_to_template,
       {'template': 'registration/activation_complete.html'},
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
       direct_to_template,
       {'template': 'registration/registration_complete.html'},
       name='registration_complete'),
   url(r'^register/closed/$',
       direct_to_template,
       {'template': 'registration/registration_closed.html'},
       name='registration_disallowed'),
   #django-registration auth urls
   url(r'^login/$',
       auth_views.login,
       {'template_name': 'registration/login.html'},
       name='auth_login'),
   url(r'^logout/$',
       auth_views.logout,
       {'template_name': 'home.html'},
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

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
