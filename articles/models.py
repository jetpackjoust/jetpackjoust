from django.db import models


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
    published = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Author(models.Model):
    """
    """
    last_name =

class Image(models.Model):
    """
    """
