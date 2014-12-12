from protorpc import messages

class ProductViewRequestMessage(messages.Message):
	name = messages.StringField(1, required=True)

class ProductViewResponseMessage(messages.Message):
	name = messages.StringField(1, required=True)
	sku = messages.StringField(2)

class ProductInsertRequestMessage(messages.Message):
	name = messages.StringField(1, required=True)
	sku = messages.StringField(2, required=True)

class ProductInsertResponseMessage(messages.Message):
	name = messages.StringField(1, required=True)
	sku = messages.StringField(2, required=True)
	data_created = messages.DateField(3)

class ProductListMessage(messages.Message):
	products = messages.MessageField(ProductViewResponseMessage, 1, repeated=True)