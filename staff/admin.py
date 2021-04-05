from django.contrib import admin
from django.contrib.admin import TabularInline
from simple_history.admin import SimpleHistoryAdmin

from staff.models import Feedback, Role, Staff

# Register your models here.
admin.site.register(Role, SimpleHistoryAdmin)
admin.site.register(Feedback, SimpleHistoryAdmin)


class FeedbackInline(TabularInline):
    model = Feedback
    can_delete = False


class RoleInline(TabularInline):
    model = Role
    can_delete = False


class StaffInline(TabularInline):
    model = Staff
    readonly_fields = ("__all__",)
    list_display_links = ["__str__"]
    exclude = (
        # "is_active",
        # "created_at",
        # "modified_at",
        # "difficulty_sort",
        # "url",
    )
    can_delete = False


class StaffAdmin(SimpleHistoryAdmin):
    list_display = ("name", "role", "supervisor", "code", "get_status_display")
    search_fields = ["code", "name"]
    list_display_links = ["name", "code"]
    list_filter = ["supervisor", "status", "role"]
    readonly_fields = ("created", "modified")
    list_select_related = ["role"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            custom_readonly_fields = (
                "created_by",
                "updated_by",
            )
            return self.readonly_fields + custom_readonly_fields
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        # TODO optimize this
        if db_field.name in ["created_by", "updated_by"]:
            requester_django_user = request.user
            kwargs["initial"] = (
                requester_django_user.staff
                if hasattr(requester_django_user, "staff")
                else None
            )
            kwargs["queryset"] = Staff.objects.filter(id=requester_django_user)
            return db_field.formfield(**kwargs)

        return super(StaffAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    class Meta:
        model = Staff


admin.site.register(Staff, StaffAdmin)


class AbstractAdmin(object):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            custom_readonly_fields = (
                "created_by",
                "updated_by",
            )
            return self.readonly_fields + custom_readonly_fields
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        # TODO optimize this
        if db_field.name in ["created_by", "updated_by"]:
            requester_django_user = request.user
            kwargs["initial"] = (
                requester_django_user.staff
                if hasattr(requester_django_user, "staff")
                else None
            )
            kwargs["queryset"] = Staff.objects.filter(id=requester_django_user)
            return db_field.formfield(**kwargs)
