import os

from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.db import models

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


def pad_date(date):
    """The variable date is a three-tuple of integers in the order year,
    month, and day.  Function pads year, month, and day with zeroes where
    appropriate and returns three-tuple of strings in same order.

    The function was created to be used in conjunction with datetime tuples.
    """
    year, month, day = date
    year = "{0:04d}".format(year)
    month = "{0:02d}".format(month)
    day = "{0:02d}".format(day)
    return (year, month, day)


def slugify_file(filename):
    """Returns string of filename slugified with extension intact.
    """
    if "." in filename:
        name = "".join(filename.split('.')[:-1])
        extension = ".{0}".format(filename.split('.')[-1].strip())
    else:
        name = filename
        extension = ""
    return "{0}{1}".format(slugify(name), extension)


class AuthorManager(models.Manager):
    """Model Manager for Author model.
    """
    use_for_related_fields = True

    def contributor(self, **kwargs):
        return self.filter(slug=kwargs['slug'])


class ArticleManager(models.Manager):
    """Model Manager for Article model.
    """
    use_for_related_fields = True

    def published(self, **kwargs):
        """kwargs contains potentially year, month, day strings as keys and
        their values.  Return all articles with published date that matches
        key values.
        """
        parameters = {'published__{0}'.format(key):
                      int(kwargs[key]) for key in kwargs}
        return self.filter(**parameters)

    def article_slug(self, slug):
        """Get article object that matches string slug.  Since slug for article
        should be unique, this should only match one article.
        """
        try:
            article = self.get(slug=slug)
        except Article.DoesNotExist:
            article = None
        return article

    def author(self, author):
        """Return Article queryset filtered on author object if it exists.
        """
        return self.filter(author=author)

    def images(self, article):
        """Return Image queryset filtered on article object if exists.
        """
        return Image.objects.filter(article=article)


class Author(models.Model):
    """Model that represents author of instance of Article model class.
    """
    last_name = models.CharField("last name of author", max_length=35)
    first_name = models.CharField("first name of author", max_length=35)
    email = models.EmailField("email address submitted for author")
    slug = models.SlugField("slug to identify author",
                            editable=False,
                            max_length=71)
    objects = AuthorManager()

    class Meta():
        ordering = ['last_name']
        app_label = 'articles'

    def save(self, *args, **kwargs):
        self.slug = slugify('{0}-{1}'.format(self.first_name,
                                             self.last_name))
        super(Author, self).save(*args, **kwargs)

    #@models.permalink
    def get_absolute_url(self):
        """Return absolute url of all articles written by author.
        """
        return reverse('show_contributor', kwargs={'slug': self.slug})

    def __str__(self):
        message = "last name: {0}, first name: {1}"
        return message.format(self.last_name, self.first_name)


class TaggedArticle(TaggedItemBase):
    """Necessary object to use non-integer based primary keys.
    """
    content_object = models.ForeignKey('Article')

    class Meta():
        app_label = 'articles'


class Article(models.Model):
    """Model that represents an article to be inserted into
    jetpackjoust.com/articles.
    """
    title = models.CharField("title of article", max_length=100,
                             primary_key=True)
    author = models.ForeignKey(Author, verbose_name="author of article")
    tags = TaggableManager(through=TaggedArticle)
    content = models.TextField("body of article")
    summary = models.TextField("summary of article")

    slug = models.SlugField("url string that points to article",
                            editable=False)
    published = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    objects = ArticleManager()

    class Meta():
        ordering = ['-published']
        app_label = 'articles'

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
        return reverse('show_article', kwargs={'year': year,
                                               'month': month,
                                               'day': day,
                                               'slug': self.slug})

    def get_tag_url(self, tag):
        return reverse('show_tag', kwargs={'slug': tag.slug})

    def get_tags_urls(self):
        """Takes each tag in self.tags and returns list of dictionaries
        containing name of tag and associated url of each tag.
        """
        tags = []
        for tag in self.tags.all():
            tags.append({'name': tag.name,
                         'url': self.get_tag_url(tag)})
        return tags

    def __str__(self):
        message = "title: {0}, author: {1}"
        return message.format(self.title, self.author)


class CoverImage(models.Model):
    """Model that represents cover image related to Album model class.
    """

    def get_image_path(instance, filename):
        """Stores file to path [media_root]/articles/images/
        year/month/day/slug/filename.
        """
        article = instance.article
        date = article.published.date().strftime('%Y-%m-%d')
        slug = str(article.slug)
        filename = slugify_file(filename)
        return os.path.join('articles', 'images', date, slug, 'cover_image',
                            filename)

    article = models.OneToOneField(Article,
                                   verbose_name="article of image")
    source = models.ImageField(verbose_name="location of image source",
                               upload_to=get_image_path)
    caption = models.CharField("caption to be used with image",
                               blank=True,
                               null=True,
                               max_length=200)

    class Meta():
        app_label = 'articles'

    def __str__(self):
        filename = str(self.source).split('/')[-1]
        message = "source: {0}, caption: {1}"
        return message.format(filename, self.caption)


class Image(models.Model):
    """Model that represents images related to Album model class.
    """
    def get_image_path(instance, filename):
        """Stores file to path [media_root]/articles/images/
        year/month/day/slug/filename.
        """
        article = instance.article
        date = article.published.date().strftime('%Y-%m-%d')
        slug = str(article.slug)
        filename = slugify_file(filename)
        return os.path.join('articles', 'images', date, slug, filename)

    article = models.ForeignKey(Article,
                                verbose_name="article to contain images")
    source = models.ImageField(verbose_name="location of image source",
                               upload_to=get_image_path)
    caption = models.CharField("caption to be used with image",
                               blank=True,
                               null=True,
                               max_length=200)

    class Meta():
        app_label = 'articles'

    def __str__(self):
        filename = str(self.source).split('/')[-1]
        title = str(self.article.title)
        message = "title: {0}, source: {1}, caption: {2}"
        return message.format(title, filename, self.caption)
