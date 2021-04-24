from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from patient.models import Patient, PatientDetail, PhoneNumber
from staff.models import Staff

# Register your models here.
# admin.site.register(Patient, SimpleHistoryAdmin)
admin.site.register(PatientDetail, SimpleHistoryAdmin)


class PhoneNumberAdmin(SimpleHistoryAdmin):
    search_fields = ["phone_number"]

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


class PatientAdmin(SimpleHistoryAdmin):
    search_fields = ["first_name", "primary_contact__phone_number", "last_name"]
    autocomplete_fields = ["phone_numbers", "primary_contact"]
    list_filter = ["gender", "locality"]
    list_display = [
        "full_name",
        "gender",
        "locality",
        "primary_assessment_sheet",
        "primary_contact",
    ]
    list_display_links = ["full_name"]


admin.site.register(Patient, PatientAdmin)
