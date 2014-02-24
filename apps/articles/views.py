from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView, ListView

from articles.models import Article, Author, TaggedArticle, Image, CoverImage
from taggit.models import Tag


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/show_article.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article_pk = context['article'].pk
        context['images'] = {article_pk:
                             Image.objects.filter(article=article_pk)}
        context['cover_image'] = {article_pk:
                                  CoverImage.objects.filter(article=article_pk)}
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
    slug_field = 'slug'

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
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        tagged_articles = TaggedArticle.objects.filter(tag_id=context['tag'].pk)
        context['articles'] = Article.objects.filter(tags=tagged_articles)
        return context


class TagListView(ListView):
    model = Tag
    template_name = 'articles/index_tags.html'

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        return context


