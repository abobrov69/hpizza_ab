# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table(u'hpizza_ab_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('restoran', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hpizza_ab.Restoran'])),
        ))
        db.send_create_signal(u'hpizza_ab', ['Product'])

        # Adding model 'ProductPortion'
        db.create_table(u'hpizza_ab_productportion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hpizza_ab.Product'])),
            ('portion', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'hpizza_ab', ['ProductPortion'])

        # Adding model 'Restoran'
        db.create_table(u'hpizza_ab_restoran', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('restoran_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'hpizza_ab', ['Restoran'])

        # Adding model 'ProductConnection'
        db.create_table(u'hpizza_ab_productconnection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hpizza_ab.Product'])),
            ('product_site_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'hpizza_ab', ['ProductConnection'])

        # Adding model 'ProductPortionConnection'
        db.create_table(u'hpizza_ab_productportionconnection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hpizza_ab.Product'])),
            ('portion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hpizza_ab.ProductPortion'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'hpizza_ab', ['ProductPortionConnection'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table(u'hpizza_ab_product')

        # Deleting model 'ProductPortion'
        db.delete_table(u'hpizza_ab_productportion')

        # Deleting model 'Restoran'
        db.delete_table(u'hpizza_ab_restoran')

        # Deleting model 'ProductConnection'
        db.delete_table(u'hpizza_ab_productconnection')

        # Deleting model 'ProductPortionConnection'
        db.delete_table(u'hpizza_ab_productportionconnection')


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
        }
    }

    complete_apps = ['hpizza_ab']