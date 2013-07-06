from django.http import HttpResponse
from django.template import RequestContext, loader

from articles.models import Article


def archive_by_year(request, year):
    """Returns list of articles archived by year.
    """
    articles = Article.objects.filter(published__year=year)
    articles = articles.order_by('-published', 'title')[:10]
    output = "\n".join([article.title for article in articles])
    return HttpResponse(output)


def archive_by_month(request, year, month):
    """Returns list of articles archived by month.
    """
    articles = Article.objects.filter(published__year=year,
                                      published__month=month)
    articles = articles.order_by('-published', 'title')[:10]
    output = "\n".join([article.title for article in articles])
    return HttpResponse(output)


def archive_by_day(request, year, month, day):
    """Returns list of articles archived by day.
    """
    articles = Article.objects.filter(published__year=year,
                                      published__month=month,
                                      published__day=day)
    articles = articles.order_by('-published', 'title')[:10]
    output = "\n".join([article.title for article in articles])
    return HttpResponse(output)


def index(request):
    latest_articles = Article.objects.order_by('-published')[:10]
    return HttpResponse("This is jousting with jetpacks.")

