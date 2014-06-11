from django.views.generic import DetailView, ListView
from articles.models import Article, Author, TaggedArticle, get_tag_url
from django.utils.datastructures import SortedDict
from taggit.models import Tag

# number of objects to include per page in paginated ListViews.
PAGINATION = 10


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
    paginate_by = PAGINATION

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
    paginate_by = PAGINATION

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
    paginate_by = PAGINATION

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        print(context.keys())
        return context


class TagDetailView(ListView):
    model = Tag
    template_name = 'articles/list_articles.html'
    paginate_by = PAGINATION

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
    paginate_by = PAGINATION

    def get_sorted_tags(self):
        """Get dictionary of tags and count of each article associated for each
        tag.  Create list of tag names and tag urls using dictionary sorted by
        count of each tag with the item with highest count first.

        Return SortedDict with tag names as keys and tag urls as values.
        """
        tags = {tag: TaggedArticle.objects.filter(tag=tag).count()
                for tag in Tag.objects.all()}

        tags_urls = [(tag.name, get_tag_url(tag))
                     for tag in sorted(tags, key=tags.get, reverse=True)]

        return SortedDict(tags_urls)

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['tags_list'] = self.get_sorted_tags()

        return context
