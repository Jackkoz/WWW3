from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reserve/', include('Pokoje.urls')),
    url(r'^template.html$', TemplateView.as_view(template_name="template.html"), name='template'),
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home')
)