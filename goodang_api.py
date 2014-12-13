from google.appengine.ext import endpoints
from protorpc import remote

from models import Item

from goodang_messages import ItemRequest
from goodang_messages import ItemResponse
from goodang_messages import ItemListRequest
from goodang_messages import ItemListResponse

CLIENT_ID = '426535775018-56vhejkglekkhtu7k73ctu1471heb3t0.apps.googleusercontent.com'

@endpoints.api(name='goodang', version='v1', description='Goodang API', allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])

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

APPLICATION = endpoints.api_server([GoodangApi], restricted=False)