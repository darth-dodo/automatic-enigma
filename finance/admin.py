from django.contrib import admin

from finance.models import Credit, Payment, PaymentMode

admin.site.register(PaymentMode)
admin.site.register(Credit)


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "appointment",
        "patient",
        "staff",
        "date",
        "mode",
        "credit",
        "payment_reference",
    ]
    list_select_related = [
        "mode",
        "credit",
        "credit__patient",
        "credit__payment_mode",
        "staff",
        "staff__role",
        "patient",
        "appointment",
        "appointment__patient",
        "appointment__staff",
        "appointment__staff__role",
        "appointment__state",
        "appointment__timeslot",
    ]
    list_filter = ["mode", "staff__role", "patient"]
    search_fields = ["staff__code", "mode__title"]
    ordering = ["-created", "-modified"]

    class Meta:
        model = Payment


admin.site.register(Payment, PaymentAdmin)
