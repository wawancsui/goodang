from google.appengine.ext import endpoints
from protorpc import message_types
from protorpc import remote

from models import Item

from goodang_messages import ItemRequest
from goodang_messages import ItemResponse
from goodang_messages import ItemListRequest
from goodang_messages import ItemListResponse

WEB_CLIENT_ID = '426535775018-56vhejkglekkhtu7k73ctu1471heb3t0.apps.googleusercontent.com'
ANDROID_CLIENT_ID = ''
IOS_CLIENT_ID = ''
ANDROID_AUDIENCE = WEB_CLIENT_ID

@endpoints.api(name='goodang', version='v1',
	description='Goodang API',
	allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
	audiences=[ANDROID_AUDIENCE],
	scopes=[endpoints.EMAIL_SCOPE])

class GoodangApi(remote.Service):
	@endpoints.method(ItemListRequest, ItemListResponse, path='items', http_method='GET', name='items.list')
	def items_get(self, request):
		query = Item.query_by_name(request)
		if request.order == ItemListRequest.Order.WHEN:
			query = query.order(-Item.date_added)
		elif request.order == ItemListRequest.Order.TEXT:
			query = query.order(Item.name)
		items = [entity.to_message() for entity in query.fetch(request.limit)]
		return ItemListResponse(items = items)

	@endpoints.method(ItemRequest, ItemResponse, path='items', http_method='POST', name='items.insert')
	def item_insert(self, request):
		entity = Item.put_from_message(request)
		return entity.to_message()

	@endpoints.method(message_types.VoidMessage, ItemResponse,
		path='authed', http_method='POST',
		name='items.authed')
	def goodang_authed(self, request):
		current_user = endpoints.get_current_user()
		email = (current_user.email() if current_user is not None
			else 'Someone')
		return Item(name='hello %s' % (email,))

APPLICATION = endpoints.api_server([GoodangApi], restricted=False)