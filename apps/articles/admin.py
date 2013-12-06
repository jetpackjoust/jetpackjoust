from django.contrib import admin
from articles.models import Author
from articles.models import Article
from articles.models import CoverImage
from articles.models import Image


class CoverImageAdminInline(admin.TabularInline):
    model = CoverImage


class ImageAdminInline(admin.TabularInline):
    model = Image


class ArticleAdmin(admin.ModelAdmin):
    inlines = (CoverImageAdminInline, ImageAdminInline)

    def get_readonly_fields(self, req, obj=None):
        """Makes primary key field 'title' read-only if this object
        is edited, otherwise, it is not if object is newly created.
        """
        if obj:
            return ('title',)
        else:
            return ()


admin.site.register(Author)
admin.site.register(CoverImage)
admin.site.register(Image)
admin.site.register(Article, ArticleAdmin)

