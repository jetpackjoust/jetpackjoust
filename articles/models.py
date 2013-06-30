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
    """Model that represents author of instance of Article model class.
    """
    last_name = models.CharField("last name of author", max_length=35)
    first_name = models.CharField("first name of author")
    email = models.EmailField("email address submitted for author")


class Image(models.Model):
    """Model that represents images related to Article model class.
    """
    title = models.ForeignKey(Article,
                              verbose_name="article related to images")
    source = model.ImageField("location of image source")
    caption = model.CharField("caption to be used with image", max_length=200)
