from django.contrib import admin
from articles.models import Author
from articles.models import Category
from articles.models import Article
from articles.models import Image

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Article, ArticleAdmin)

