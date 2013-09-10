from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from articles.models import Article, Image, TaggedArticle
from taggit.models import Tag

from utils.paginator import DiggPaginator

NUMBER_PER_PAGE = 10

def index_articles(request, **kwargs):
    """Returns list of articles archived by filtering parameters
    passed in kwargs.
    """

    filter_parameters = {"published__{0}".format(key):
                         int(kwargs[key]) for key in kwargs}

    if filter_parameters:
        articles = Article.objects.filter(**filter_parameters)
    else:
        articles = Article.objects.all()

    articles = articles.order_by('-published', 'title')


    paginator = DiggPaginator(articles, NUMBER_PER_PAGE, body=5,
                              padding=2, margin=2)

    page = request.GET.get('page')
    # Default to first page if no parameters is passed.
    if not page:
        page = 1

    try:
        articles = paginator.page(page)
    except(PageNotAnInteger):
        # If page is not an integer, default to first page.
        articles = paginator.page(1)
    except(EmptyPage):
        # If page is out of range, default to last page.
        articles = paginator.page(paginator.num_pages)

    template = loader.get_template('articles/index_articles.html')
    context = RequestContext(request, {
            'articles': articles
            })
    return HttpResponse(template.render(context))


def index_tags(request):
    """Returns list of all tags in database and links to said tags.
    """
    tags = []
    for tag in Tag.objects.all().order_by('name'):
        tags.append({'name': tag.name,
                     'url': '/'.join(['/articles', 'tags', tag.slug])})

    template = loader.get_template('articles/index_tags.html')
    context = RequestContext(request, {
            'tags': tags,
            })
    return HttpResponse(template.render(context))


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
    articles = Article.objects.filter(tags__slug__iexact = tag_slug)
    articles = articles.order_by('-published', 'title')

    paginator = DiggPaginator(articles, NUMBER_PER_PAGE, body=5,
                              padding=1, margin=2)

    page = request.GET.get('page')
    # Default to first page if no parameters is passed.
    if not page:
        page = 1

    try:
        articles = paginator.page(page)
    except(PageNotAnInteger):
        # If page is not an integer, default to first page.
        articles = paginator.page(1)
    except(EmptyPage):
        # If page is out of range, default to last page.
        articles = paginator.page(paginator.num_pages)

    template = loader.get_template('articles/index_articles.html')
    context = RequestContext(request, {
            'articles': articles,
            })
    return HttpResponse(template.render(context))

