import os
import sys
from os.path import dirname, join, normpath, realpath
sys.path.append(dirname(dirname(realpath(__file__))))

from models import Author, TaggedArticle, Article, CoverImage, Image
