import pytest
from app import app
from pymongo import MongoClient
import os

# test POST request to /products, returns 405 error
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_invalid_route_method(client):
    response = client.post('/products')
    assert response.status_code == 405


# test connection to mongo db
@pytest.fixture
def mongo_client():
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
    mongo_client = MongoClient(f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.8sk8t.mongodb.net/?retryWrites=true&w=majority")
    return mongo_client

# Test 2: test database read
def test_mongo_ping(mongo_client):
    db = mongo_client["shop_db"]
    server_info = mongo_client.server_info()
    assert server_info is not None

# Test 3: test database write inserting test product
def test_insert_product(mongo_client):
    db = mongo_client["shop_db"]
    products_collection = db["products"]

    # test data
    new_product = {
        "name": "Test Knife",
        "tag": "test",
        "price": "99.99",
        "image_path": "static/images/knife1.jpg"
    }

    products_collection.insert_one(new_product)

    # confirm  product was inserted
    inserted_product = products_collection.find_one({"name": "Test Knife"})
    assert inserted_product is not None
    assert inserted_product['name'] == "Test Knife"
    assert inserted_product['price'] == "99.99"

