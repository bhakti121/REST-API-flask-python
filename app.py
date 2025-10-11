from flask import Flask,request

app = Flask(__name__)

#for storing data in memory
#for now we are not using any database
#we will use a list of dictionaries to store our data
#each store will be a dictionary with name and items
#each item will be a dictionary with name and price
#[{}, {}]
stores = [
    { 
        "name":"my store",
        "items": [{
            "name":"chair",
            "price":15.99
        }]

    }
]

@app.get("/stores")     #http://127.0.0.1:5000/stores
def get_stores():
    return {"stores": stores}

@app.post("/stores")
def create_store():
    request_data= request.get_json()
    new_store = {"name": request_data["name"],"items": []}
    stores.append(new_store)
    return new_store,201


@app.post("/stores/<string:name>/items")
def create_item_in_store(name):
    request_data=request.get_json()
    for store in stores:
        if store["name"]== name:
            new_item={ "name": request_data["name"],"price": request_data["price"]}
            store["items"].append(new_item)
            return new_item,201
    return {"message":"store not found"},404


@app.get("/stores/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"]== name:
            return store
    return {"message":"store not found"},404

@app.get("/stores/<string:name>/items")

