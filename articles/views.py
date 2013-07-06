from django.http import HttpResponse
from django.template import RequestContext, loader

from articles.models import Article


def archive_by_year(request, article_year):
    """Returns list of articles archived by year.
    """

def archive_by_month(request, article_year, article_month):
    """Returns list of articles archived by month.
    """

def archive_by_day(request, article_year, article_month, article_day):
    """Returns list of articles archived by day.
    """


def index(request):
    latest_articles = Article.objects.order_by('-published')[:10]
    return HttpResponse("This is jousting with jetpacks.")

