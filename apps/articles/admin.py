from django.contrib import admin
from articles.models import Author
from articles.models import Category
from articles.models import Article
from articles.models import Image


class ImageAdminInline(admin.TabularInline):
    model = Image


class ArticleAdmin(admin.ModelAdmin):
    inlines = (ImageAdminInline,)

    def get_readonly_fields(self, req, obj=None):
        """Makes primary key field 'title' read-only if this object
        is edited, otherwise, it is not if object is newly created.
        """
        if obj:
            return ('title',)
        else:
            return ()


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Article, ArticleAdmin)

