from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from appointment.models import Appointment, FollowUp, State, TimeSlot

admin.site.register(TimeSlot, SimpleHistoryAdmin)
admin.site.register(State, SimpleHistoryAdmin)
admin.site.register(Appointment, SimpleHistoryAdmin)
admin.site.register(FollowUp, SimpleHistoryAdmin)
