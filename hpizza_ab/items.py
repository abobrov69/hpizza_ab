# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from models import Product, ProductConnection, ProductPortion, ProductPortionConnection, Restoran
from django.core.exceptions import ObjectDoesNotExist

class HPizzaItem(Item):
    # define the fields for your item here like:
    # name = Field()
    id = Field()
    name = Field()
    value = Field()
    size = Field()

class GnsDjangoItem(DjangoItem):

    def get_item(self):
        modelargs = dict((k, self.get(k)) for k in self._values
                         if k in self._model_fields)
        try:
            model = self.django_model._default_manager.filter(**modelargs).get()
        except ObjectDoesNotExist:
            model = None
        return model

class ProductItem(DjangoItem):
    django_model = Product

class ProductConnectionItem(DjangoItem):
    django_model = ProductConnection

class ProductPortionItem(DjangoItem):
    django_model = ProductPortion

class ProductPortionConnectionItem(DjangoItem):
    django_model = ProductPortionConnection

class RestoranItem(DjangoItem):
    django_model = Restoran