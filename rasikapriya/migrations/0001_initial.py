# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Instrument'
        db.create_table(u'rasikapriya_instrument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='name', unique_with=())),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'rasikapriya', ['Instrument'])

        # Adding model 'Artist'
        db.create_table(u'rasikapriya_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='full_name', unique_with=())),
            ('native_place', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('home_page', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'rasikapriya', ['Artist'])

        # Adding M2M table for field band_members on 'Artist'
        m2m_table_name = db.shorten_name(u'rasikapriya_artist_band_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_artist', models.ForeignKey(orm[u'rasikapriya.artist'], null=False)),
            ('to_artist', models.ForeignKey(orm[u'rasikapriya.artist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_artist_id', 'to_artist_id'])

        # Adding model 'Venue'
        db.create_table(u'rasikapriya_venue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='full_address', unique_with=())),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('home_page', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'rasikapriya', ['Venue'])

        # Adding model 'Organization'
        db.create_table(u'rasikapriya_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='name', unique_with=())),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rasikapriya.Venue'], null=True, blank=True)),
            ('home_page', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'rasikapriya', ['Organization'])

        # Adding model 'Festival'
        db.create_table(u'rasikapriya_festival', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='full_name', unique_with=())),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rasikapriya.Organization'], null=True, blank=True)),
            ('home_page', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rasikapriya.Venue'], null=True, blank=True)),
        ))
        db.send_create_signal(u'rasikapriya', ['Festival'])

        # Adding model 'Concert'
        db.create_table(u'rasikapriya_concert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('festival', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rasikapriya.Festival'], null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rasikapriya.Organization'], null=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['rasikapriya.Venue'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('cached_venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rasikapriya.Venue'])),
        ))
        db.send_create_signal(u'rasikapriya', ['Concert'])

        # Adding model 'Performance'
        db.create_table(u'rasikapriya_performance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rasikapriya.Artist'])),
            ('concert', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rasikapriya.Concert'])),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rasikapriya.Instrument'])),
        ))
        db.send_create_signal(u'rasikapriya', ['Performance'])


    def backwards(self, orm):
        # Deleting model 'Instrument'
        db.delete_table(u'rasikapriya_instrument')

        # Deleting model 'Artist'
        db.delete_table(u'rasikapriya_artist')

        # Removing M2M table for field band_members on 'Artist'
        db.delete_table(db.shorten_name(u'rasikapriya_artist_band_members'))

        # Deleting model 'Venue'
        db.delete_table(u'rasikapriya_venue')

        # Deleting model 'Organization'
        db.delete_table(u'rasikapriya_organization')

        # Deleting model 'Festival'
        db.delete_table(u'rasikapriya_festival')

        # Deleting model 'Concert'
        db.delete_table(u'rasikapriya_concert')

        # Deleting model 'Performance'
        db.delete_table(u'rasikapriya_performance')


    models = {
        u'rasikapriya.artist': {
            'Meta': {'object_name': 'Artist'},
            'band_members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['rasikapriya.Artist']", 'symmetrical': 'False', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'home_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'native_place': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'full_name'", 'unique_with': '()'})
        },
        u'rasikapriya.concert': {
            'Meta': {'object_name': 'Concert'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['rasikapriya.Artist']", 'through': u"orm['rasikapriya.Performance']", 'symmetrical': 'False'}),
            'cached_venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rasikapriya.Venue']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'festival': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rasikapriya.Festival']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rasikapriya.Organization']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['rasikapriya.Venue']"})
        },
        u'rasikapriya.festival': {
            'Meta': {'object_name': 'Festival'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'home_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rasikapriya.Organization']", 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'full_name'", 'unique_with': '()'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rasikapriya.Venue']", 'null': 'True', 'blank': 'True'})
        },
        u'rasikapriya.instrument': {
            'Meta': {'object_name': 'Instrument'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        },
        u'rasikapriya.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'home_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rasikapriya.Venue']", 'null': 'True', 'blank': 'True'})
        },
        u'rasikapriya.performance': {
            'Meta': {'object_name': 'Performance'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rasikapriya.Artist']"}),
            'concert': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rasikapriya.Concert']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rasikapriya.Instrument']"})
        },
        u'rasikapriya.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'home_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'full_address'", 'unique_with': '()'})
        }
    }

    complete_apps = ['rasikapriya']