from django.http import HttpResponse
from articles.models import Article

def index(request):
    return HttpResponse("This is jousting with jetpacks.")
