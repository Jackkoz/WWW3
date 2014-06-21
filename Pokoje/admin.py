from django.contrib import admin

from Pokoje.models import Room, FreeTerm, Reservation, Attribute


# Register your models here.


admin.site.register(Room)
admin.site.register(FreeTerm)
admin.site.register(Reservation)
admin.site.register(Attribute)