from google.appengine.ext import endpoints
from google.appengine.ext import ndb

from goodang_messages import ItemResponse



DEFAULT_PRODUCT = 'default_product'
TIME_FORMAT_STRING = '%b %d, %Y %I:%M:%S %p'

def get_endpoints_current_user(raise_unauthorized=True):
	current_user = endpoints.get_current_user()
	if raise_unauthorized and current_user is None:
		raise endpoints.UnauthorizedException('Invalid token')
	return current_user

def product_key(product_name):
	print 'produk namanya = ' + product_name
	return ndb.Key('Item', product_name)

# [START item]
class Item(ndb.Model):
	"""Models an individual item entry"""
	creator = ndb.UserProperty()
	name = ndb.StringProperty(indexed=True)
	sku = ndb.StringProperty(indexed=True)

	date_added = ndb.DateTimeProperty(auto_now_add=True)
	date_modified = ndb.DateTimeProperty(auto_now=True)

	@property
	def timestamp_date_added(self):
		return self.date_added.strftime(TIME_FORMAT_STRING)

	@property
	def timestamp_date_modified(self):
		return self.date_modified.strftime(TIME_FORMAT_STRING)

#	@classmethod
	def to_message(self):
		return ItemResponse(id=self.key.id(), name = self.name,
			sku = self.sku)

	@classmethod
	def put_from_message(cls, message):
		current_user = get_endpoints_current_user()
		entity = cls(parent=product_key(message.product_name or DEFAULT_PRODUCT),
			creator=current_user, name=message.name, sku=message.sku)
		entity.put()
		return entity

	@classmethod
	def query_by_name(cls, message):
		return cls.query(cls.name == message.name)
# [END item]