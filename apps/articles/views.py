from django.views.generic import DetailView, ListView
from articles.models import Article, Author
from taggit.models import Tag


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/show_article.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = context['article']
        context['tags_urls'] = article.get_tags_urls()
        context['images'] = Article.objects.images(article)

        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list_articles.html'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.published(**self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['tags_urls'] = {article: article.get_tags_urls()
                                for article in context['article_list']}

        return context


class AuthorDetailView(ListView):
    model = Author
    template_name = 'articles/list_articles.html'

    def get_queryset(self):
        author = Author.objects.contributor(**self.kwargs)
        return Article.objects.author(author=author)

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['tags_urls'] = {article: article.get_tags_urls()
                                for article in context['article_list']}

        return context


class AuthorListView(ListView):
    model = Author
    template_name = 'articles/list_contributors.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        return context


class TagDetailView(ListView):
    model = Tag
    template_name = 'articles/list_articles.html'

    def get_queryset(self):
        tag = Tag.objects.filter(slug=self.kwargs['slug'])
        return Article.objects.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['tags_urls'] = {article: article.get_tags_urls()
                                for article in context['article_list']}

        return context


class TagListView(ListView):
    model = Tag
    template_name = 'articles/list_tags.html'

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        return context
