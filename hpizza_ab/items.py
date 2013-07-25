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
    _key_fields = []

    def __init__(self, *args, **kwargs):
        super (DjangoItem,self).__init__(*args,**kwargs)
        for i,fld in enumerate(self._key_fields):
            if not fld in self._model_fields:
                self._key_fields.pop(i)
        if not self._key_fields: self._key_fields = [self.fields[0]]
        self._not_key_fields = [fld for fld in self._key_fields if fld not in self._model_fields]

    def read(self):
        key_value = {}
        for fld in self._key_fields:
            if fld in self._values:
                key_value[fld]=self._values[fld]
            else:
                raise ValueError('ReadItem: Value of key field "%s" is not defined' % fld)
        try:
            obj = self.django_model._default_manager.filter(**key_value).get()
            for fld in self._not_key_fields:
                self.__setitem__(fld,obj.__getattribute__(fld))
        except ObjectDoesNotExist:
            obj = None
        return obj

    def save(self, commit=True):
        model = self.read()
        if not model
            modelargs = dict((k, self.get(k)) for k in self._values
                         if k in self._model_fields)
            model = self.django_model(**modelargs)

        if commit:
            model.save()
        return model









        modelargs = dict((k, self.get(k)) for k in self._values
                         if k in self._model_fields)
            model = self.django_model._default_manager.filter(**modelargs).get()
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