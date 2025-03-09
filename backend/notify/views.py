from django.http import HttpResponse
from .main import send_sms


def index(request):
    html = '<html lang="en"><body><button type="button">Click Me!</button></body></html>'
    send_sms("s")
    return HttpResponse(html)