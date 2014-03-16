from django.core.management.base import BaseCommand
from optparse import make_option

from articles.test_articles.test_models import TaggedArticleTwoTagsFactory
from articles.test_articles.test_models import AuthorFactory
from articles.test_articles.test_models import TagFactory
from articles.test_articles.test_models import ImageFactory


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-r', '--rows',
                    action='store',
                    type=int,
                    dest='rows',
                    default=10,
                    help='Create number of instances of models supplied.'),)

    def handle(self, *args, **options):
        """Create tagged article model instance for number of times specified
        in options['rows'] for one author with same tags.
        """
        rows = options['rows']

        author = AuthorFactory()
        tag_1 = TagFactory()
        tag_2 = TagFactory()

        for i in range(rows):
            ImageFactory(article=TaggedArticleTwoTagsFactory(tag_1=tag_1,
                                                             tag_2=tag_2,
                                                             author=author))
