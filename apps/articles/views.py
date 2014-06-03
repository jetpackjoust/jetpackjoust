from django.views.generic import DetailView, ListView
from articles.models import Article, Author, TaggedArticle
from taggit.models import Tag


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/show_article.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = context['article']
        context['tags_urls'] = article.get_tags_urls()
        context['cover_image'] = Article.objects.cover_image(article)
        context['images'] = Article.objects.images(article)
        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list_articles.html'

    def get_queryset(self):
        return Article.objects.published(**self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['cover_images'] = {article:
                                   Article.objects.cover_image(article)
                                   for article in context['article_list']}
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'articles/show_contributor.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.author(author=context['author'])
        context['tags_urls'] = {article: article.get_tags_urls()
                                for article in context['articles']}
        context['cover_images'] = {article:
                                   Article.objects.cover_image(article=article)
                                   for article in context['articles']}
        return context


class AuthorListView(ListView):
    model = Author
    template_name = 'articles/list_contributors.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        return context


class TagDetailView(DetailView):
    model = Tag
    template_name = 'articles/show_tag.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        tagged_articles = TaggedArticle.objects.filter(tag_id=
                                                       context['tag'])
        context['articles'] = Article.objects.filter(tags=tagged_articles)
        context['tags_urls'] = {article: article.get_tags_urls()
                                for article in context['articles']}
        context['cover_images'] = {article:
                                   Article.objects.cover_image(article=article)
                                   for article in context['articles']}
        return context


class TagListView(ListView):
    model = Tag
    template_name = 'articles/list_tags.html'

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        return context
