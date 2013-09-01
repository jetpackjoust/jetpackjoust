from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from articles.models import Article, Image, TaggedArticle
from taggit.models import Tag


def index(request):
    latest_articles = Article.objects.order_by('-published')
    template = loader.get_template('articles/index.html')
    context = RequestContext(request, {
            'latest_articles': latest_articles,
            })
    return HttpResponse(template.render(context))


def index_by_year(request, year):
    """Returns list of articles archived by year.
    """
    articles = Article.objects.get(published__year=year)
    articles = articles.order_by('-published', 'title')
    output = "\n".join([article.title for article in articles])
    return HttpResponse(output)


def index_by_month(request, year, month):
    """Returns list of articles archived by month.
    """
    articles = Article.objects.get(published__year=year,
                                      published__month=month)
    articles = articles.order_by('-published', 'title')
    output = "\n".join([article.title for article in articles])
    return HttpResponse(output)


def index_by_day(request, year, month, day):
    """Returns list of articles archived by day.
    """
    articles = Article.objects.get(published__year=year,
                                      published__month=month,
                                      published__day=day)
    articles = articles.order_by('-published', 'title')
    output = "\n".join([article.title for article in articles])
    return HttpResponse(output)


def index_tags(request):
    """Returns list of all tags in database and links to said tags.
    """
    tags = []
    for tag in Tag.objects.all():
        tags.append({'name': tag.name,
                     'url': '/'.join(['/articles', 'tags', tag.slug])})
    output = "\n".join([str(tag) for tag in tags])
    return HttpResponse(output)


def show_article(request, slug):
    """Displays article that has the provided slug using the show_article
    template.
    """
    article =  get_object_or_404(Article, slug=slug)

    images = Image.objects.filter(article=article)

    tags = article.get_tags_urls()

    template = loader.get_template('articles/show_article.html')
    context = RequestContext(request, {
            'article': article,
            'images': images,
            'tags': tags
            })
    return HttpResponse(template.render(context))


def show_tag(request, tag_slug):
    """Displays list of links to articles that have the associated tag_slug.
    """
    output = ""
    return HttpResponse(output)

