from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option

from articles.test_articles.test_models import TaggedArticleTwoTagsFactory
from articles.test_articles.test_models import TaggedArticleThreeTagsFactory

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-r', '--rows',
                    action='store',
                    type = int,
                    dest = 'rows',
                    default = 10,
                    help = 'Create number of instances of models supplied.'),
        )

    def handle(self, *args, **options):
        """Create tagged article model instance for number of times specified
        in options['rows']
        """
        for i in range(options['rows']):
            TaggedArticleTwoTagsFactory()
