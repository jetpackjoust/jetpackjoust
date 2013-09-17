from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, get_list_or_404

from articles.models import Author, Article, Image, TaggedArticle
from taggit.models import Tag

from utils.paginator import DiggPaginator, get_page_request as get_page


def index_articles(request, **kwargs):
    """Returns list of articles archived by filtering parameters
    passed in kwargs.
    """

    filter_parameters = {"published__{0}".format(key):
                         int(kwargs[key]) for key in kwargs}

    if filter_parameters:
        articles = get_list_or_404(Article.objects.filter(**filter_parameters))
    else:
        articles = get_list_or_404(Article.objects.all())

    articles = get_page(articles, request)

    template = loader.get_template('articles/index_articles.html')
    context = RequestContext(request, {
            'articles': articles
            })
    return HttpResponse(template.render(context))


def index_contributors(request):
    """Display links to all contributors on the site.
    """
    authors = get_list_or_404(Author.objects.all())
    authors = get_page(authors, request)

    template = loader.get_template('articles/index_contributors.html')
    context = RequestContext(request, {
            'authors': authors
            })
    return HttpResponse(template.render(context))


def index_tags(request):
    """Returns list of all tags in database and links to said tags.
    """
    tag_list = get_list_or_404(Tag.objects.all().order_by('name'))

    tags = []

    for tag in tag_list:
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


def show_contributor(request, contributor_slug):
    """Displays all articles written by contributor as identified
    by contributor_slug.
    """
    articles = get_list_or_404(Article.objects
                               .filter(author__contributor_slug__iexact=
                                       contributor_slug))

    articles = get_page(articles, request)

    template = loader.get_template('articles/index_articles.html')
    context = RequestContext(request, {
            'articles': articles
            })
    return HttpResponse(template.render(context))


def show_tag(request, tag_slug):
    """Displays list of links to articles that have the associated tag_slug.
    """
    articles = get_list_or_404(Article.objects.filter(tags__slug__iexact=
                                                      tag_slug))

    articles = get_page(articles, request)

    template = loader.get_template('articles/index_articles.html')
    context = RequestContext(request, {
            'articles': articles,
            })
    return HttpResponse(template.render(context))

