from django.contrib import admin

from finance.models import Credit, Payment, PaymentMode

admin.site.register(PaymentMode)
admin.site.register(Credit)
admin.site.register(Payment)
