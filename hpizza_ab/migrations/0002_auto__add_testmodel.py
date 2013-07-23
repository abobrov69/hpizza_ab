# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestModel'
        db.create_table(u'hpizza_ab_testmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'hpizza_ab', ['TestModel'])


    def backwards(self, orm):
        # Deleting model 'TestModel'
        db.delete_table(u'hpizza_ab_testmodel')


    models = {
        u'hpizza_ab.product': {
            'Meta': {'object_name': 'Product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'restoran': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hpizza_ab.Restoran']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'hpizza_ab.productconnection': {
            'Meta': {'object_name': 'ProductConnection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hpizza_ab.Product']"}),
            'product_site_id': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'hpizza_ab.productportion': {
            'Meta': {'object_name': 'ProductPortion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hpizza_ab.Product']"})
        },
        u'hpizza_ab.productportionconnection': {
            'Meta': {'object_name': 'ProductPortionConnection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hpizza_ab.ProductPortion']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hpizza_ab.Product']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'hpizza_ab.restoran': {
            'Meta': {'object_name': 'Restoran'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'restoran_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'hpizza_ab.testmodel': {
            'Meta': {'object_name': 'TestModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['hpizza_ab']