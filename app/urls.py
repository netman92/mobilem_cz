# project wide urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.contrib import admin
admin.autodiscover()
import settings

# import your urls from each app here, as needed
import mobilem_api.urls

urlpatterns = patterns('',

    # urls specific to this app
    url(r'^mobilem_api/', include(mobilem_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # catch all, redirect to mobilem_api home view
    url(r'.*', RedirectView.as_view(url='/mobilem_api/home')),

)
