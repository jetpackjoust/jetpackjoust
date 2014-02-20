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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertEqual(response.context_data['article'].pk, self.article.pk)
