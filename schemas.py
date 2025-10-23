from marshmallow import schema,fields

class ItemSchema(schema):
    id=fields.Str(dump_only=True)
    name =fields.Str(required=True)
    price=fields.Float(required=True)
    store_id=fields.Str(required=True)    

class ItemUpdateSchema(schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)