import datetime

import pytz
from django.core.management.utils import get_random_secret_key
from django.http import JsonResponse


def ping(request):
    data = dict()
    data["ping"] = "pong"
    data["timestamp"] = datetime.datetime.now(
        tz=pytz.timezone("Asia/Kolkata")
    ).isoformat()
    data["random_string"] = get_random_secret_key()
    return JsonResponse(data)


def trigger_error(request):
    division_by_zero = 1 / 0
