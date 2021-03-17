from django.contrib import admin

from appointment.models import Appointment, FollowUp, State, TimeSlot

admin.site.register(TimeSlot)
admin.site.register(State)
admin.site.register(Appointment)
admin.site.register(FollowUp)
