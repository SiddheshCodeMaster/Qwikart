from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/welcomeQwikart")
def root():
    return {"message":"Hello User, welcome to Qwikart..."} 

@app.get("/get_all_products")
def get_products():
    return {
        "product_data": {
            "Tropicana Natural Fresh Orange Juice": {
                "Price": 80,
                "Description": "Tropicana Natural Fresh Orange Juice, 100 percent Fresh and made up of real oranges",
                "Quantity": 100
            },
            "Prime USA Energy Drink": {
                "Price": 330,
                "Description": "Prime USA Energy Drink: KSI Flavour",
                "Quantity": 50
            }
        }
    }

@app.post("/createProducts")
def create_products(payloadProduct : dict = Body(...)):
    
    # Process the incoming data to store in the required structure
    added_products = []
    for product_name, information in payloadProduct.items():
        added_products.append({
            "product_name": product_name,
            "information": information
        })

    return {"added_products": added_products}

