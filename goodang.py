import os
# import cgi
import urllib

from google.appengine.api import users
# [START import_ndb]
from google.appengine.ext import ndb
# [END import_ndb]

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

#MAIN_PAGE_FOOTER_TEMPLATE = """\
#	<form action="/product?%s" method="post">
#		<div><textarea name="productname" rows="1" cols="60"></textarea></div>
#		<div><textarea name="productsku" rows="1" cols="60"></textarea></div>
#		<div><input type="submit" value="Save Product"></div>
#	</form>
#	<hr>
#	<form>Your product:
#		<input value="%s" name="category_name">
#		<input type="submit" value="switch">
#	</form>
#	<a href="%s">%s</a>
#	</body>
#	</html>
#"""

DEFAULT_PRODUCT = 'default_product'

def product_key(product_name=DEFAULT_PRODUCT):
	return ndb.Key('Product', product_name)

# [START item]
class Item(ndb.Model):
	"""Models an individual item entry"""
	creator = ndb.UserProperty()
	name = ndb.StringProperty(indexed=True)
	sku = ndb.StringProperty(indexed=True)

	date_added = ndb.DateTimeProperty(auto_now_add=True)
	date_modified = ndb.DateTimeProperty(auto_now=True)
# [END item]

# [START main_page]
class MainPage(webapp2.RequestHandler):
	def get(self):
#		self.response.write('<html><body>')
		product_name = self.request.get('product_name', DEFAULT_PRODUCT)

		# [START query]
		item_query = Item.query(ancestor=product_key(product_name)).order(-Item.date_added)
		items = item_query.fetch(10)
		# [END query]


#		for item in items:
#			if item.creator:
#				self.response.write(
#					'<b>%s</b> added:' % item.creator.nickname())
#			else:
#				self.response.write('Someone added:')
#			self.response.write('<blockquote>%s</blockquote>' %
#				cgi.escape(item.name))

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'login'

		template_values = {
			'items': items,
			'product_name': urllib.quote_plus(product_name),
			'url': url,
			'url_linktext': url_linktext,
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))
		# Write the add item form and the footer of the page
#		item_query_param = urllib.urlencode({'product_name': product_name})
#		self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %
#			(item_query_param, cgi.escape(product_name),
#				url, url_linktext))
# [END main_page]

# [START product]
class Product(webapp2.RequestHandler):
	def post(self):

		product_name = self.request.get('product_name', DEFAULT_PRODUCT)
		item = Item(parent=product_key(product_name))

		if users.get_current_user():
			item.creator = users.get_current_user()

		item.name = self.request.get('productname')
		item.sku = self.request.get('productsku')
		item.put()

		query_params = {'products': product_name}
		self.redirect('/?' + urllib.urlencode(query_params))
# [END product]

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/product', Product),
], debug=True)