import unittest

from django.core.urlresolvers import reverse
from django.test import RequestFactory

import apps.articles.models as models
import apps.articles.urls as urls
import apps.articles.views as views
import apps.articles.test_articles.test_models as test_models


class TestArticleDetailView(unittest.TestCase):
    """Tests related to view ArticleDetailView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.article = test_models.TaggedArticleTwoTagsFactory()
        self.image_list = [test_models.ImageFactory(article=self.article)
                           for i in range(3)]
        self.images = self.image_list
        self.cover_image = test_models.CoverImageFactory(article=self.article)
        self.template_name = views.ArticleDetailView.template_name
        self.url_parameters = {'year': "{0:04d}".format(self.article.published.year),
                               'month': "{0:02d}".format(self.article.published.month),
                               'day': "{0:02d}".format(self.article.published.day),
                               'slug': self.article.slug}

    def test_details(self):
        """Test to be certain that view returns desired object in context_data,
        correct template name, and returns a status code of 200 for a
        successful GET HTTP response.
        """
        url = reverse('show_article', urlconf=urls, kwargs=self.url_parameters)

        request = self.factory.get(url)

        view = views.ArticleDetailView.as_view()

        response = view(request, slug=self.article.slug)
        context_data = response.context_data

        article = context_data['article']
        cover_image = context_data['cover_image']
        images = context_data['images']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertEqual(article.pk, self.article.pk)
        self.assertEqual(cover_image, self.cover_image)
        self.assertEqual(set([i.pk for i in images]),
                         set([i.pk for i in self.images]))


class TestAuthorDetailView(unittest.TestCase):
    """Tests related to view AuthorDetailView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.author = test_models.AuthorFactory()
        self.template_name = views.AuthorDetailView.template_name
        self.url_parameters = {'slug': self.author.slug}
        self.articles = [test_models.ArticleFactory(author=self.author) for
                         i in range(5)]
        self.cover_images = {article:
                             test_models.CoverImageFactory(article=article)
                             for article in self.articles}

    def test_details(self):
        """Test to be certain that view returns desired object in context_data,
        correct template name, and returns a status code of 200 for a
        successful GET HTTP response.
        """
        url = reverse('show_contributor', urlconf=urls, kwargs=self.url_parameters)

        request = self.factory.get(url)

        view = views.AuthorDetailView.as_view()

        response = view(request, slug=self.author.slug)
        articles = response.context_data['articles']
        cover_images = response.context_data['cover_images']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertEqual(response.context_data['author'].pk, self.author.pk)
        self.assertEqual(set([a.pk for a in articles]),
                         set([a.pk for a in self.articles]))
        self.assertEqual(cover_images, self.cover_images)


class TestTagDetailView(unittest.TestCase):
    """Tests related to view TagDetailView.
    """
    def setUp(self):
        tagged_article = models.TaggedArticle
        article = models.Article

        self.factory = RequestFactory()
        self.tag = test_models.TagFactory()
        self.template_name = views.TagDetailView.template_name
        self.url_parameters = {'slug': self.tag.slug}

        """Create 5 TaggedArticle instances with tag self.tag"""
        for i in range(5):
            test_models.TaggedArticleFactory(tag=self.tag)

        self.tagged_articles = tagged_article.objects.filter(tag_id=self.tag.id)
        self.articles = article.objects.filter(tags=self.tagged_articles)
        self.cover_images = {article:
                             test_models.CoverImageFactory(article=article)
                             for article in self.articles}

    def test_details(self):
        """Test to be certain that view returns desired object in context_data,
        correct template name, and returns a status code of 200 for a
        successful GET HTTP response.
        """
        url = reverse('show_tag', urlconf=urls, kwargs=self.url_parameters)

        request = self.factory.get(url)

        view = views.TagDetailView.as_view()

        response = view(request, slug=self.tag.slug)
        context = response.context_data
        articles = response.context_data['articles']
        cover_images = context['cover_images']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertEqual(context['tag'].pk, self.tag.pk)
        self.assertEqual(set([a.pk for a in articles]),
                         set([a.pk for a in self.articles]))
        self.assertEqual(cover_images, self.cover_images)
