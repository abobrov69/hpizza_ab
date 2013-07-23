# -*- coding: utf-8 -*-

from django.db import models

class TestModel(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=25)

class Product(models.Model):
    title = models.CharField(max_length=255) # Название блюда,  в рамках задачи считать сочитание полей title и restoran_id уникальным
    price = models.IntegerField() # Цена наименьшей порции
    restoran = models.ForeignKey("Restoran") # Ресторан, из которого взято блюдо (создайте модель самостоятельно).

class ProductPortion(models.Model):
    product = models.ForeignKey("Product")
    portion = models.CharField(max_length = 255) # Название порции. Например, 25cм, 35см, 45см, 400г, 681г, 1.2кг,  8 штук, 36 штук, ¼, ½ , ¾,
    price = models.IntegerField() # Цена порции.

class Restoran(models.Model):
    restoran_name = models.CharField(max_length=255)

class ProductConnection(models.Model):
    product = models.ForeignKey('Product')
    product_site_id = models.CharField(max_length=10)

class ProductPortionConnection(models.Model):
    product = models.ForeignKey('Product')
    portion = models.ForeignKey('ProductPortion')
    value = models.CharField(max_length=10)
