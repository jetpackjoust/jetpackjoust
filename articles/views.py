from django.http import HttpResponse
from django.template import RequestContext, loader

from articles.models import Article


def archive_by_year(request, year):
    """Returns list of articles archived by year.
    """
    return HttpResponse("This is jousting with jetpacks by year.")


def archive_by_month(request, year, month):
    """Returns list of articles archived by month.
    """
    return HttpResponse("This is jousting with jetpacks by month.")


def archive_by_day(request, year, month, day):
    """Returns list of articles archived by day.
    """
    return HttpResponse("This is jousting with jetpacks by day.")


def index(request):
    latest_articles = Article.objects.order_by('-published')[:10]
    return HttpResponse("This is jousting with jetpacks.")

