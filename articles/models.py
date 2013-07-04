import os
from django.db import models


class Author(models.Model):
    """Model that represents author of instance of Article model class.
    """
    last_name = models.CharField("last name of author", max_length=35)
    first_name = models.CharField("first name of author", max_length=35)
    email = models.EmailField("email address submitted for author")

    def __str__(self):
        message =  "last name: {0}, first name: {1}"
        return message.format(self.last_name, self.first_name)


class Article(models.Model):
    """Model that represents an article to be inserted into
    jetpackjoust.com/articles.
    """
    title = models.CharField("title of article", max_length=70,
                             primary_key=True)
    author = models.ForeignKey(Author, verbose_name="author of article")
    content = models.TextField("body of article")
    summary = models.TextField("summary of article")
    category = models.CharField("sub category of article", max_length=20)
    url = models.CharField("url string that points to article",
                           max_length=50)
    published = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        message =  "title: {0}, author: {1}"
        return message.format(self.title, self.author)


class Image(models.Model):
    """Model that represents images related to Article model class.
    """
    def get_image_path(instance, filename):
        """Stores file to path /articles/images/url/filename.
        """
        return os.path.join('articles', 'images', str(instance.title.url),
                            filename)

    title = models.ForeignKey(Article,
                              verbose_name="article related to images")
    caption = models.CharField("caption to be used with image", max_length=200)
    source = models.ImageField("location of image source",
                               upload_to=get_image_path)

    def __str__(self):
        message =  "{0}, caption: {1}"
        return message.format(self.title, self.caption)
