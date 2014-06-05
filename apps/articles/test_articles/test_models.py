from datetime import datetime
import os
import random
import unittest

from django.utils.text import slugify
import factory
from factory.fuzzy import FuzzyNaiveDateTime
import taggit.models

import apps.articles.models as models


email_template = "{0}.{1}@example.com"
slug_t = "{0}-{1}"
cover_image = 'test image 1.jpg'
image = 'test image 2.jpg'


def random_word(n):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    return ''.join([random.choice(letters) for i in range(n)])


class AuthorFactory(factory.django.DjangoModelFactory):
    """Factory for model Author in articles app.
    """
    FACTORY_FOR = models.Author

    last_name = factory.Sequence(lambda n: "Test last name {0}".format(n))
    first_name = factory.Sequence(lambda n: "Test first name {0}".format(n))

    email = factory.LazyAttribute(lambda n: email_template.format(n.first_name,
                                                                  n.last_name))

    slug = factory.LazyAttribute(lambda n: slugify(slug_t.format(n.first_name,
                                                                 n.last_name)))


class ArticleFactory(factory.django.DjangoModelFactory):
    """Factory for model Article in articles app.
    """
    FACTORY_FOR = models.Article

    title = factory.Sequence(lambda n: "{0}".format(random_word(20)))
    author = factory.SubFactory(AuthorFactory)
    content = factory.Sequence(lambda n: "Test content {0}".format(n))
    summary = factory.Sequence(lambda n: "Test summary {0}".format(n))
    slug = factory.LazyAttribute(lambda n: slugify(n.title))
    published = FuzzyNaiveDateTime(datetime(2012, 1, 1))
    last_modified = factory.LazyAttribute(lambda n: n.published)


class TagFactory(factory.django.DjangoModelFactory):
    """Factory for taggit.models Tag.
    """
    FACTORY_FOR = taggit.models.Tag

    name = factory.Sequence(lambda n: "Test tag {0}".format(n))
    slug = factory.LazyAttribute(lambda n: slugify(n.name))


class CoverImageFactory(factory.django.DjangoModelFactory):
    """Factory for model Cover Image in articles app
    """
    FACTORY_FOR = models.CoverImage

    article = factory.SubFactory(ArticleFactory)
    source = factory.django.ImageField(from_path=os.path.join(os.getcwd(),
                                                              'development',
                                                              'test_images',
                                                              cover_image))
    caption = factory.Sequence(lambda n: "Test caption {0}".format(n))


class ImageFactory(factory.django.DjangoModelFactory):
    """Factory for model Image in articles app
    """
    FACTORY_FOR = models.Image

    article = factory.SubFactory(ArticleFactory)
    source = factory.django.ImageField(from_path=os.path.join(os.getcwd(),
                                                              'development',
                                                              'test_images',
                                                              image))
    caption = factory.Sequence(lambda n: "Test caption {0}".format(n))


class TaggedArticleFactory(factory.django.DjangoModelFactory):
    """Factory for through model that links many to many tags to articles.
    """
    FACTORY_FOR = models.TaggedArticle

    tag = factory.SubFactory(TagFactory)
    content_object = factory.SubFactory(ArticleFactory)


class TaggedArticleTwoTagsFactory(ArticleFactory):
    """Factory that returns Article object and creates related tags.
    """
    tag_1 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')
    tag_2 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')


class TaggedArticleThreeTagsFactory(ArticleFactory):
    """Factory that returns Article object and creates related tags.
    """
    tag_1 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')
    tag_2 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')
    tag_3 = factory.RelatedFactory(TaggedArticleFactory, 'content_object')


class TestPadDate(unittest.TestCase):
    """Tests function articles.models.pad_date that adds takes datetime tuples
    and returns tuple of strings with padded zeroes to create pretty dates.
    """
    def setUp(self):
        self.date_1 = (2013, 1, 1)
        self.date_2 = (2013, 11, 11)

    def test_pad_date(self):
        padded_date_1 = models.pad_date(self.date_1)
        padded_date_2 = models.pad_date(self.date_2)
        self.assertEqual(('2013', '01', '01'), padded_date_1)
        self.assertEqual(('2013', '11', '11'), padded_date_2)


class TestSlugifyFile(unittest.TestCase):
    """Tests function articles.models.slugify_file to ensure that the
    string filename gets returned slugified and with extension intact.
    """
    def setUp(self):
        self.none = "manning face"
        self.single = "manning face.png"
        self.multiple = "manning . face. png"

    def test_slugify_file(self):
        slugified_none = models.slugify_file(self.none)
        slugified_single = models.slugify_file(self.single)
        slugified_multiple = models.slugify_file(self.multiple)
        self.assertEqual("manning-face", slugified_none)
        self.assertEqual("manning-face.png", slugified_single)
        self.assertEqual("manning-face.png", slugified_multiple)


class TestArticle(unittest.TestCase):
    """Tests related to model articles.models.Article.
    """
    def setUp(self):
        self.today = datetime.today()
        self.article = TaggedArticleThreeTagsFactory()

    def test_get_absolute_url(self):
        url_parameters = [self.today.year,
                          self.today.month,
                          self.today.day,
                          self.article.slug]
        url = '/articles/{0}/{1:02d}/{2:02d}/{3}'.format(*url_parameters)
        self.assertEqual(url, self.article.get_absolute_url())

    def test_get_tags_urls(self):
        template = '/articles/tags/{0}'
        tags = [{'name': tag.name, 'url': template.format(slugify(str(tag)))}
                for tag in self.article.tags.all()]
        self.assertEqual(tags, self.article.get_tags_urls())

    def test_slugify(self):
        self.assertEqual(slugify(self.article.title), self.article.slug)


class TestArticleManager(unittest.TestCase):
    """Tests related to model manager for model articles.models.Article.
    """
    def setUp(self):
        self.article = ArticleFactory()
        self.cover_image = CoverImageFactory(article=self.article)
        self.images = [ImageFactory(article=self.article) for i in range(3)]
        self.dates = {'year': self.article.published.year,
                      'month': self.article.published.month,
                      'day': self.article.published.day}
        self.slug = self.article.slug

    def test_published(self):
        model_set = models.Article.objects.published(**self.dates)
        manager_set = models.Article.objects.published(**self.dates)
        model_pks = [obj.pk for obj in model_set]
        manager_pks = [obj.pk for obj in manager_set]
        self.assertEqual(model_pks, manager_pks)

    def test_article_slug(self):
        model = models.Article.objects.get(slug=self.slug)
        manager = models.Article.objects.article_slug(slug=self.slug)
        manager_empty = models.Article.objects.article_slug(slug='made-up')
        self.assertEqual(model.pk, manager.pk)
        self.assertEqual(None, manager_empty)

    def test_author(self):
        model = models.Article.objects.filter(author=self.article.author)
        manager = models.Article.objects.author(author=self.article.author)
        non_existant_pk = self.article.author.pk + 1
        manager_empty = models.Article.objects.author(author=non_existant_pk)
        self.assertEqual([obj.pk for obj in model],
                         [obj.pk for obj in manager])
        self.assertEqual(False, manager_empty.exists())

    def test_images(self):
        model = models.Image.objects.filter(article=self.article)
        manager = models.Article.objects.images(article=self.article)
        manager_empty = models.Article.objects.images(article='Made up')
        self.assertEqual([obj.pk for obj in model],
                         [obj.pk for obj in manager])
        self.assertEqual(False, manager_empty.exists())


class TestAuthor(unittest.TestCase):
    """Tests related to model articles.models.Author.
    """
    def setUp(self):
        self.author = AuthorFactory(last_name="Gauss", first_name="Carl")

    def test_get_absolute_url(self):
        url = '/articles/contributors/carl-gauss'
        self.assertEqual(url, self.author.get_absolute_url())

    def test_slugify(self):
        self.assertEqual("carl-gauss", self.author.slug)


class TestAuthorManager(unittest.TestCase):
    """Tests related to model manager for model articles.models.Author.
    """
    def setUp(self):
        self.author = AuthorFactory(last_name="Reed", first_name="Ed")
        self.slugs = {"slug": "ed-reed"}

    def test_contributor_filter(self):
        slug = self.slugs['slug']
        model_set = models.Author.objects.filter(slug=slug)
        manager_set = models.Author.objects.contributor(**self.slugs)
        model_pks = [obj.pk for obj in model_set]
        manager_pks = [obj.pk for obj in manager_set]
        self.assertEqual(model_pks, manager_pks)


class TestCoverImage(unittest.TestCase):
    """Tests related to model articles.models.CoverImage.
    """
    def setUp(self):
        self.cover_image = CoverImageFactory()

    def test_get_image_path(self):
        date_string = self.cover_image.article.published.date()
        date_string = date_string.strftime('%Y-%m-%d')
        slug = self.cover_image.article.slug
        location = os.path.join('articles', 'images', date_string, slug,
                                'cover_image', 'test-image-1.jpg')
        result = self.cover_image.get_image_path('test image 1.jpg')
        self.assertEqual(location, result)


class TestImage(unittest.TestCase):
    """Tests related to model articles.models.Image.
    """
    def setUp(self):
        self.image = ImageFactory()

    def test_get_image_path(self):
        date_string = self.image.article.published.date().strftime('%Y-%m-%d')
        slug = self.image.article.slug
        location = os.path.join('articles', 'images', date_string, slug,
                                'test-image-2.jpg')
        result = self.image.get_image_path('test image 2.jpg')
        self.assertEqual(location, result)
