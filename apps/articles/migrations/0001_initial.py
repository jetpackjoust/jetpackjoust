# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table('articles_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('contributor_slug', self.gf('django.db.models.fields.SlugField')(max_length=71)),
        ))
        db.send_create_signal('articles', ['Author'])

        # Adding model 'TaggedArticle'
        db.create_table('articles_taggedarticle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles_taggedarticle_items', to=orm['taggit.Tag'])),
            ('content_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Article'])),
        ))
        db.send_create_signal('articles', ['TaggedArticle'])

        # Adding model 'Article'
        db.create_table('articles_article', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Author'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('published', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('articles', ['Article'])

        # Adding model 'CoverImage'
        db.create_table('articles_coverimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['articles.Article'], unique=True)),
            ('source', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('articles', ['CoverImage'])

        # Adding model 'Image'
        db.create_table('articles_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(related_name='article', to=orm['articles.Article'])),
            ('source', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('articles', ['Image'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('articles_author')

        # Deleting model 'TaggedArticle'
        db.delete_table('articles_taggedarticle')

        # Deleting model 'Article'
        db.delete_table('articles_article')

        # Deleting model 'CoverImage'
        db.delete_table('articles_coverimage')

        # Deleting model 'Image'
        db.delete_table('articles_image')


    models = {
        'articles.article': {
            'Meta': {'ordering': "['-published']", 'object_name': 'Article'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Author']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        'articles.author': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Author'},
            'contributor_slug': ('django.db.models.fields.SlugField', [], {'max_length': '71'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        'articles.coverimage': {
            'Meta': {'object_name': 'CoverImage'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['articles.Article']", 'unique': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'articles.image': {
            'Meta': {'object_name': 'Image'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'article'", 'to': "orm['articles.Article']"}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'articles.taggedarticle': {
            'Meta': {'object_name': 'TaggedArticle'},
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles_taggedarticle_items'", 'to': "orm['taggit.Tag']"})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['articles']