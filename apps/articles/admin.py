from django.contrib import admin
from articles.models import Album
from articles.models import Author
from articles.models import Article
from articles.models import Image


class ImageAdminInline(admin.TabularInline):
    model = Image


class ArticleAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, req, obj=None):
        """Makes primary key field 'title' read-only if this object
        is edited, otherwise, it is not if object is newly created.
        """
        if obj:
            return ('title',)
        else:
            return ()


class AlbumAdmin(admin.ModelAdmin):
    inlines = (ImageAdminInline, )


admin.site.register(Album, AlbumAdmin)
admin.site.register(Author)
admin.site.register(Image)
admin.site.register(Article, ArticleAdmin)

