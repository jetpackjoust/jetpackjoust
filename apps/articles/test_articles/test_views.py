import unittest

from django.core.urlresolvers import reverse
from django.test import RequestFactory

import apps.articles.models as models
import apps.articles.urls as urls
import apps.articles.views as views
import apps.articles.test_articles.test_models as test


def get_request(request_factory, url_name, urlconf, url_parameters):
    """Return HTTP response object using supplied RequestFactory.  Create url
    object using reverse() with string url_name, url configuration model
    urlconf, and dict url_parameters containing keywords to be used in urlconf
    and corresponding values.
    """
    url = reverse(url_name, urlconf=urlconf, kwargs=url_parameters)
    return request_factory.get(url)


class TestArticleDetailView(unittest.TestCase):
    """Tests related to view ArticleDetailView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.tag = test.TagFactory()
        test.TaggedArticleFactory(tag=self.tag)
        self.tagged_articles = models.TaggedArticle.objects.filter(tag_id=
                                                                   self.tag.id)
        self.article = models.Article.objects.get(tags=self.tagged_articles)

        self.tags_urls = self.article.get_tags_urls()
        self.cover_image = test.CoverImageFactory(article=self.article)
        self.images = [test.ImageFactory(article=self.article)
                       for i in range(3)]
        self.published = self.article.published

        self.template_name = 'articles/show_article.html'
        self.view = views.ArticleDetailView.as_view()
        self.url_name = 'show_article'
        self.url_parameters = {'year': "{0:04d}".format(self.published.year),
                               'month': "{0:02d}".format(self.published.month),
                               'day': "{0:02d}".format(self.published.day),
                               'slug': self.article.slug}

    def test_missing_context(self):
        """Make sure that if cover_image or images does not exist that
        page loads as expected.
        """
        tag = test.TagFactory()
        test.TaggedArticleFactory(tag=tag)
        queryset = models.TaggedArticle.objects.filter(tag_id=tag.id)
        article = models.Article.objects.get(tags=queryset)
        published = article.published

        request = get_request(self.factory, self.url_name, urls,
                              {'year': "{0:04d}".format(published.year),
                               'month': "{0:02d}".format(published.month),
                               'day': "{0:02d}".format(published.day),
                               'slug': article.slug})

        response = self.view(request, slug=article.slug)
        context = response.context_data

        self.assertEqual(None, context['cover_image'])
        self.assertEqual(False, context['images'].exists())

    def test_context(self):
        """Test to be certain that view returns desired objects in
        context_data, correct template name, and returns a status code of
        200 for a successful GET HTTP response.
        """
        request = get_request(self.factory, self.url_name, urls,
                              self.url_parameters)

        response = self.view(request, slug=self.article.slug)
        context = response.context_data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertEqual(context['article'].pk, self.article.pk)
        self.assertEqual(context['tags_urls'], self.tags_urls)
        self.assertEqual(context['cover_image'], self.cover_image)
        self.assertEqual(set([i.pk for i in context['images']]),
                         set([i.pk for i in self.images]))


class TestAuthorDetailView(unittest.TestCase):
    """Tests related to view AuthorDetailView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.author = test.AuthorFactory()
        self.template_name = views.AuthorDetailView.template_name

        self.articles = [test.ArticleFactory(author=self.author) for
                         i in range(3)]
        self.tags_urls = {article: article.get_tags_urls()
                          for article in self.articles}
        self.cover_images = {article: test.CoverImageFactory(article=article)
                             for article in self.articles}

        self.template_name = 'articles/show_contributor.html'
        self.view = views.AuthorDetailView.as_view()
        self.url_name = 'show_contributor'
        self.url_parameters = {'slug': self.author.slug}

    def test_missing_context(self):
        """Make sure that if cover_images do not exist that page loads as
        expected.
        """
        author = test.AuthorFactory()

        request = get_request(self.factory, self.url_name, urls,
                              {'slug': author.slug})

        response = self.view(request, slug=author.slug)
        context = response.context_data

        for article in context['cover_images']:
            self.assertEqual(None, context['cover_images'][article])

    def test_context(self):
        """Test to be certain that view returns desired object in context_data,
        correct template name, and returns a status code of 200 for a
        successful GET HTTP response.
        """
        request = get_request(self.factory, self.url_name, urls,
                              self.url_parameters)

        response = self.view(request, slug=self.author.slug)
        context = response.context_data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertEqual(context['author'], self.author)
        self.assertEqual(set([a.pk for a in context['articles']]),
                         set([a.pk for a in self.articles]))
        self.assertEqual(context['tags_urls'], self.tags_urls)
        self.assertEqual(context['cover_images'], self.cover_images)


class TestTagDetailView(unittest.TestCase):
    """Tests related to view TagDetailView.
    """
    def setUp(self):
        tagged_article = models.TaggedArticle
        article = models.Article

        self.factory = RequestFactory()
        self.tag = test.TagFactory()

        """Create 3 TaggedArticle instances with tag - self.tag"""
        for i in range(3):
            test.TaggedArticleFactory(tag=self.tag)

        self.tagged_articles = tagged_article.objects.filter(tag_id=
                                                             self.tag.id)
        self.articles = article.objects.filter(tags=self.tagged_articles)
        self.tags_urls = {article: article.get_tags_urls()
                          for article in self.articles}
        self.cover_images = {article:
                             test.CoverImageFactory(article=article)
                             for article in self.articles}

        self.template_name = 'articles/show_tag.html'
        self.view = views.TagDetailView.as_view()
        self.url_name = 'show_tag'
        self.url_parameters = {'slug': self.tag.slug}

    def test_missing_context(self):
        """Make sure that if cover_images do not exist that page loads as
        expected.
        """
        tag = test.TagFactory()

        request = get_request(self.factory, self.url_name, urls,
                              {'slug': tag.slug})

        response = self.view(request, slug=tag.slug)
        context = response.context_data

        for article in context['cover_images']:
            self.assertEqual(None, context['cover_images'][article])

    def test_context(self):
        """Test to be certain that view returns desired objects in
        context_data, correct template name, and returns a status code of
        200 for a successful GET HTTP response.
        """
        request = get_request(self.factory, self.url_name, urls,
                              self.url_parameters)

        response = self.view(request, slug=self.tag.slug)
        context = response.context_data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertEqual(context['tag'], self.tag)
        self.assertEqual(set([a.pk for a in context['articles']]),
                         set([a.pk for a in self.articles]))
        self.assertEqual(context['tags_urls'], self.tags_urls)
        self.assertEqual(context['cover_images'], self.cover_images)
