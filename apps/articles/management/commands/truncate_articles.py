from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option

from articles.models import Article, TaggedArticle, Author, Image, CoverImage
from taggit.models import Tag, TaggedItem

class Command(BaseCommand):

    def handle(self, *args, **options):
        """Create tagged article model instance for number of times specified
        in options['rows']
        """
        Article.objects.all().delete()
        TaggedArticle.objects.all().delete()
        Author.objects.all().delete()
        Image.objects.all().delete()
        CoverImage.objects.all().delete()
        Tag.objects.all().delete()
        TaggedItem.objects.all().delete()

