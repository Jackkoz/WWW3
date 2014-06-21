from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^login$', 'Pokoje.views.userlogin', name='userlogin'),
    url(r'^logout$', 'Pokoje.views.userlogout', name='userlogout'),
    url(r'^list/$', 'Pokoje.views.room_list', name='list'),
    url(r'^search$', 'Pokoje.views.search', name="search"),
    url(r'^reservations', 'Pokoje.views.reservations', name='reservations'),
    url(r'^list/get/(?P<room_id>\d+)$', "Pokoje.views.room", name='room'),
    url(r'^term/get/(?P<room_id>\d+)$', 'Pokoje.views.term', name='term'),
    url(r'^ajax_term/get/(?P<room_id>\d+)$', 'Pokoje.views.ajax_term', name='ajax_term'),
    url(r'^confirm$', 'Pokoje.views.confirm', name='confirm'),
    url(r'^ajax_confirm$', 'Pokoje.views.ajax_confirm', name='ajax_confirm'),
    url(r'^success$', 'Pokoje.views.success', name='success'),
)