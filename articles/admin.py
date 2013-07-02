from django.contrib import admin
from articles.models import Author
from articles.models import Article
from articles.models import Image

admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Image)
