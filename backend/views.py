from django.http import JsonResponse
import datetime
import pytz

def ping(request):
    data = dict()
    data["ping"] = "pong"
    data["timestamp"] = datetime.datetime.now(tz=pytz.timezone("Asia/Kolkata")).isoformat()
    return JsonResponse(data)