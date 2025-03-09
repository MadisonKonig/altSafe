from django.http import HttpResponse
from .services.queue import start_scheduler


def index(request):
    html = '<html lang="en"><body><button type="button">Click Me!</button></body></html>'
    start_scheduler(1)
    return HttpResponse(html)