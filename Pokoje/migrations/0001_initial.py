# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attribute'
        db.create_table('Pokoje_attribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('Pokoje', ['Attribute'])

        # Adding model 'Room'
        db.create_table('Pokoje_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Pokoje', ['Room'])

        # Adding M2M table for field attributes on 'Room'
        m2m_table_name = db.shorten_name('Pokoje_room_attributes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('room', models.ForeignKey(orm['Pokoje.room'], null=False)),
            ('attribute', models.ForeignKey(orm['Pokoje.attribute'], null=False))
        ))
        db.create_unique(m2m_table_name, ['room_id', 'attribute_id'])

        # Adding model 'FreeTerm'
        db.create_table('Pokoje_freeterm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Pokoje.Room'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('begin', self.gf('django.db.models.fields.IntegerField')()),
            ('end', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Pokoje', ['FreeTerm'])

        # Adding model 'Reservation'
        db.create_table('Pokoje_reservation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Pokoje.Room'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('begin', self.gf('django.db.models.fields.IntegerField')()),
            ('end', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Pokoje', ['Reservation'])


    def backwards(self, orm):
        # Deleting model 'Attribute'
        db.delete_table('Pokoje_attribute')

        # Deleting model 'Room'
        db.delete_table('Pokoje_room')

        # Removing M2M table for field attributes on 'Room'
        db.delete_table(db.shorten_name('Pokoje_room_attributes'))

        # Deleting model 'FreeTerm'
        db.delete_table('Pokoje_freeterm')

        # Deleting model 'Reservation'
        db.delete_table('Pokoje_reservation')


    models = {
        'Pokoje.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'Pokoje.freeterm': {
            'Meta': {'object_name': 'FreeTerm'},
            'begin': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Pokoje.Room']"})
        },
        'Pokoje.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'begin': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Pokoje.Room']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'Pokoje.room': {
            'Meta': {'object_name': 'Room'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['Pokoje.Attribute']"}),
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Pokoje']