from google.appengine.ext import endpoints
from google.appengine.ext import ndb

from goodang_message import ProductViewResponseMessage

TIME_FORMAT_STRING = '%b %d, %Y %I:%M:%S %p'
DEFAULT_PRODUCT_KEY = 'default'

def product_key(product_category=DEFAULT_PRODUCT_KEY):
	return ndb.Key('Product', product_category)

class Product(ndb.Model):
	
	name = ndb.StringProperty(required=True)
	sku = ndb.StringProperty(required=True)

	date_created = ndb.DateTimeProperty(auto_now_add=True)
	last_updated = ndb.DateTimeProperty(auto_now=True)


	def _get_kind(cls):
		return 'Product'

	@property
	def date_created_timestamp(self):
		return self.date_created.strftime(TIME_FORMAT_STRING)

	@property
	def last_updated_timestamp(self):
		return self.last_updated.strftime(TIME_FORMAT_STRING)

	@classmethod
	def add_new_product(cls, message):
		entity = cls(parent=product_key(DEFAULT_PRODUCT_KEY), name=message.name, sku=message.sku)
		entity.put()
		return entity

	@classmethod
	def query_product(cls, message):
		return cls.query(ancestor=product_key(message.category), cls.name == message.name)

	def to_message(self):
		return ProductViewResponseMessage(id=self.key.id(), name=self.name, sku=self.sku)