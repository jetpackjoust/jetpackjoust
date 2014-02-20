from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import DetailView, ListView

from articles.models import Article, Author, TaggedArticle
from taggit.models import Tag

from utils.paginator import DiggPaginator, get_page


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/show_article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/index_articles.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'articles/index_contributors.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        return context


class AuthorListView(ListView):
    model = Author
    template_name = 'articles/index_contributors.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        return context


class TagDetailView(DetailView):
    model = Tag
    template_name = 'articles/show_tag.html'

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        tagged_articles = TaggedArticle.objects.filter(tag_id=context['tag'].id)
        context['articles'] = Article.objects.filter(tags=tagged_articles)
        return context


class TagListView(ListView):
    model = Tag
    template_name = 'articles/index_tags.html'

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        return context


