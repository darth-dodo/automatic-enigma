from django.contrib import admin

from patient.models import Patient, PatientDetail, PhoneNumber
from staff.models import Staff

# Register your models here.
# admin.site.register(PhoneNumber)
admin.site.register(Patient)
admin.site.register(PatientDetail)


class PhoneNumberAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "phone_number_created_by":
            kwargs["queryset"] = Staff.objects.filter(username=request.user.username)
        return super(PhoneNumberAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ("created_by",)
        return self.readonly_fields


admin.site.register(PhoneNumber, PhoneNumberAdmin)
