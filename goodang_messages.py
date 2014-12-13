from protorpc import messages

class ItemRequest(messages.Message):
	name = messages.StringField(1, required=True)
	sku = messages.StringField(2, required=True)
	product_name = messages.StringField(3)

class ItemResponse(messages.Message):
	id = messages.IntegerField(1)
	name = messages.StringField(2)
	sku = messages.StringField(3)

class ItemListRequest(messages.Message):
	name = messages.StringField(1, required=True)
	limit = messages.IntegerField(2, default=10)
	class Order(messages.Enum):
		WHEN = 1
		TEXT = 2
	order = messages.EnumField(Order, 3, default=Order.WHEN)

class ItemListResponse(messages.Message):
	items = messages.MessageField(ItemResponse, 1, repeated=True)