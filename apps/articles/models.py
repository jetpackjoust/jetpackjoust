import os
import re
from django.conf import settings
from django.utils.text import slugify
from django.db import models

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


def pad_date(date):
    """The variable date is a three-tuple of integers in the order year,
    month, and day.  Function pads year, month, and day with zeroes where
    appropriate and returns three-tuple of strings in same order.
    """
    year, month, day = date
    year = "{0:04d}".format(year)
    month = "{0:02d}".format(month)
    day = "{0:02d}".format(day)
    return (year, month, day)


class Author(models.Model):
    """Model that represents author of instance of Article model class.
    """
    last_name = models.CharField("last name of author", max_length=35)
    first_name = models.CharField("first name of author", max_length=35)
    email = models.EmailField("email address submitted for author")
    contributor_slug = models.CharField("slug to identify author",
                                        max_length=71)

    def save(self, *args, **kwargs):
        self.contributor_slug = slugify(u'{0}-{1}'.format(self.first_name,
                                                          self.last_name))
        super(Author, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url of all articles written by author.
        """
        url = '/'.join(['/articles', 'contributors', self.contributor_slug])
        return url

    def __str__(self):
        message = "last name: {0}, first name: {1}"
        return message.format(self.last_name, self.first_name)


class TaggedArticle(TaggedItemBase):
    """Necessary object to use non-integer based primary keys.
    """
    content_object = models.ForeignKey('Article')


class Article(models.Model):
    """Model that represents an article to be inserted into
    jetpackjoust.com/articles.
    """
    title = models.CharField("title of article", max_length=100,
                             primary_key=True)
    author = models.ForeignKey(Author, verbose_name="author of article")
    content = models.TextField("body of article")
    summary = models.TextField("summary of article")

    slug = models.SlugField("url string that points to article",
                            editable=False)
    tags = TaggableManager(through=TaggedArticle)
    published = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Since title will only be created once, we can save the slug
        as the title each time on save without worrying about the slug used
        to create the permalink ever changing as the title cannot be changed.
        """
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url of article.
        """
        date = self.published.date().timetuple()[:3]
        year, month, day = pad_date(date)
        url = '/'.join(['/articles', year, month, day, self.slug])
        return url

    def get_tags_urls(self):
        """Takes each tag in self.tags and returns list of dictionaries
        containing name of tag and associated url of each tag.
        """
        tags = []
        for tag in self.tags.all():
            tags.append({'name': tag.name,
                         'url': '/'.join(['/articles', 'tags', tag.slug])})
        return tags

    def __str__(self):
        message =  "title: {0}, author: {1}"
        return message.format(self.title, self.author)


class Image(models.Model):
    """Model that represents images related to Article model class.
    """

    def get_image_path(instance, filename):
        """Stores file to path [media_root]/articles/images/
        year/month/day/slug/filename.
        """
        date = instance.article.published.date().timetuple()[:3]
        year, month, day = pad_date(date)
        return os.path.join('articles', 'images', year, month, day,
                        str(instance.article.slug), filename)

    article = models.ForeignKey(Article,
                              verbose_name="article related to images")
    caption = models.CharField("caption to be used with image", max_length=200)
    source = models.ImageField("location of image source",
                               upload_to=get_image_path)

    def __str__(self):
        message =  "{0}, caption: {1}"
        return message.format(self.article, self.caption)
