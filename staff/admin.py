from django.contrib import admin

from staff.models import Feedback, Role, Staff

# Register your models here.
admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(Feedback)
