from protorpc import messages_type
from protorpc import remote

import goodang

class PostService(remote.Service):
	# Add the remote decorator to indicate the service method
	@remote.method(Item, messages_types.VoidMessage)
	def post_item(self, request):
		item = goodang.Item(name=request.name, sku=request.sku)
		item.put()
		return messages_types.VoidMessage()