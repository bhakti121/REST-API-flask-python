from flask import Flask
from flask_smorest import Api
import os
from flask_sqlalchemy import SQLAlchemy
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
import models   #importing models to create tables before the first request
from db import db

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True         #to propagate exceptions even if debug is false
    app.config["API_TITLE"] = "Stores REST API"       #title of the API
    app.config["API_VERSION"] = "v1"                  #version of the API
    app.config["OPENAPI_VERSION"] = "3.0.3"           #OpenAPI version
    app.config["OPENAPI_URL_PREFIX"] = "/"            #prefix for the OpenAPI documentation
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"               #path for the Swagger UI
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"         #URL for the Swagger UI
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")    #getting the database url from environment variable if not found use sqlite database ,how? it will look for DATABASE_URL in .env file"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"    #getting the database url from environment variable if not found use sqlite database ,how? it will look for DATABASE_URL in .env file"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False       #to disable the Flask-SQLAlchemy event system which is unnecessary and adds overhead , set it to false to save resources,which is recommended by the Flask-SQLAlchemy documentation, which means it will not track modifications of objects and emit signals
    

    db.init_app(app)    #initialize the SQLAlchemy instance with the Flask app what is init_app? it is a method of SQLAlchemy class that initializes the app with the database settings
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app


































######### added everying below this line initially in app.py for basic CURD operations without using MethodView and Blueprints ##########
######## now the code below is commented out as we have refactored the code using MethodView and Blueprints in resources/item.py and resources/store.py ##########

# from flask import Flask,request
# from db import stores,items
# from flask_smorest import abort
# import uuid
# app = Flask(__name__)

# #CURD operations for stores and items

# @app.get("/stores")
# def get_stores():
#     return {"stores": list(stores.values())}    

# @app.get("/stores/<string:store_id>")            #get specific store by id
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except IndexError:
#         abort(404, message="store not found")


# @app.post("/stores")
# def create_store():
#     stores_data = request.get_json()
#     if "name" not in stores_data:
#         abort(400, message="Bad request. 'name' is a required field.") #using abort from flask_smorest to handle bad request, replace - return {"message": "Bad request. 'name' is a required field."}, 400

#     for store in stores.values():
#         if store["name"] == stores_data["name"]:
#             abort(400, message=f"store with name '{stores_data['name']}' already exists.") #using abort from flask_smorest to handle bad request, replace - return {"message": f"store with name '{stores_data['name']}' already exists."}, 400
    
#     store_id = uuid.uuid4().hex     #generating unique id for each store
#     new_store={**stores_data, "id": store_id}     #unpacking the stores_data dictionary and adding id key-value pair , replacing    new_store = {"id": store_id, "name": stores_data["name"], "items": []}
#     stores[store_id] = stores
#     return stores, 201

# @app.delete("/stores/<string:store_id>")     #delete specific store by id
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "store deleted"}
#     except KeyError:
#         abort(404, message="store not found")

# @app.put("/stores/<string:store_id>")        #update specific store by id
# def update_store(store_id):
#     new_store_data = request.get_json()
#     if "name" not in new_store_data:          #if name field is missing
#         abort(400, message="Bad request. 'name' is a required field.") #using abort from flask_smorest to handle bad request, replace - return {"message": "Bad request. 'name' is a required field."}, 400

#     try:
#         old_store = stores[store_id]   #explaining this line - getting the store from the stores dictionary using the store_id
#         old_store.update(new_store_data)  #explaining this line - updating the store with the new data from new_store_data dictionary
#         return old_store
#     except KeyError:
#         abort(404, message="store not found")



# @app.get("/items")
# def get_items():
#     return {"items": list(items.values())}

# @app.get("/items/<string:item_id>")        #get specific item by id
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message="item not found")

# @app.post("/items")
# def create_item():
#     item_data= request.get_json()
#     if ("name" not in item_data) or ("price" not in item_data) or ("store_id" not in item_data):
#         abort(400, message="Bad request. 'name', 'price' and 'store_id' are required fields.") #using abort from flask_smorest to handle bad request, replace - return {"message": "Bad request. 'name', 'price' and 'store_id' are required fields."}, 400

#     if item_data["store_id"] not in stores:
#         abort(404, message="store not found") #using abort from flask_smorest to handle not found, replace - return {"message": "store not found"}, 404
    
#     for item in items.values():
#         if (item_data["name"] == item["name"]
#         and item_data["store_id"] == item["store_id"]):
#             abort(400, message=f"item with name '{item_data['name']}' already exists in store '{item_data['store_id']}'") #using abort from flask_smorest to handle bad request, replace - return {"message": f"item with name '{item_data['name']}' already exists in store '{item_data['store_id']}'"}, 400
    
#     item_id = uuid.uuid4().hex
#     new_item = {**item_data, "id": item_id}   #replacing new_item = {"id": item_id, "name": item_data["name"], "price": item_data["price"], "store_id": item_data["store_id"]}
#     items[item_id] = new_item
#     return new_item, 201
       
# @app.delete("/items/<string:item_id>")     #delete specific item by id
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "item deleted"}
#     except KeyError:
#         abort(404, message="item not found")


# @app.put("/items/<string:item_id>")        #update specific item by id
# def update_item(item_id):
#     new_item_data = request.get_json()
#     if ("name" not in new_item_data) or ("price" not in new_item_data) or ("store_id" not in new_item_data):          #if any of the fields are missing
#         abort(400, message="Bad request. 'name', 'price' and 'store_id' are required fields.") #using abort from flask_smorest to handle bad request, replace - return {"message": "Bad request. 'name', 'price' and 'store_id' are required fields."}, 400

#     if new_item_data["store_id"] not in stores:
#         abort(404, message="store not found") #using abort from flask_smorest to handle not found, replace - return {"message": "store not found"}, 404
    
#     try:
#         old_item = items[item_id]   #explaining this line - getting the item from the items dictionary using the item_id
#         old_item.update(new_item_data)  #explaining this line - updating the item with the new data from new_item_data dictionary
#         return old_item
#     except KeyError:
#         abort(404, message="item not found")










# """#for storing data in memory
# #for now we are not using any database
# #we will use a list of dictionaries to store our data
# #each store will be a dictionary with name and items
# #each item will be a dictionary with name and price
# #[{}, {}]
# stores = [
#     { 
#         "name":"my store",
#         "items": [{
#             "name":"chair",
#             "price":15.99
#         }]

#     }
# ]""" #commenting this as we are using db.py now we can store it in the form of dictionary

# # @app.get("/stores")     #http://127.0.0.1:5000/stores
# # def get_stores():
# #     return {"stores": stores}
   

# # @app.post("/stores")
# # def create_store():
# #     request_data= request.get_json()
# #     new_store = {"name": request_data["name"],"items": []}
# #     stores.append(new_store)
# #     return new_store,201

# # @app.post("/stores/<string:name>/items")
# # def create_item_in_store(name):
# #     request_data=request.get_json()
# #     for store in stores:
# #         if store["name"]== name:
# #             new_item={ "name": request_data["name"],"price": request_data["price"]}
# #             store["items"].append(new_item)
# #             return new_item,201
# #     return {"message":"store not found"},404

# # @app.get("/stores/<string:name>")
# # def get_store(name):
# #     for store in stores:
# #         if store["name"]== name:
# #             return store
# #     return {"message":"store not found"},404
    
# # @app.get("/stores/<string:name>/items")
# # def get_items_in_store(name):
# #     for store in stores:
# #         if store["name"]== name:
# #             return {"items": store["items"]}
# #     return {"message":"store not found"},404


#  ########################