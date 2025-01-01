from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello User, welcome to Qwikart..."} 

@app.get("/get_all_products")
def get_products():
    return {"product_data": {"product":[{"Tropicana Natural Fresh Orange Juice":
                                        {"Price":80, 
                                         "Description":"Tropicana Natural Fresh Orange Juice, 100 percent Fresh and made up of real oranges",
                                         "Quantity": 100}},
                                         {"Prime USA Energy Drink":
                                            {"Price":330, 
                                            "Description":"Prime USA Energy Drink: KSI Flavour",
                                            "Quantity": 50}}
                                        ]
                            }
            }
