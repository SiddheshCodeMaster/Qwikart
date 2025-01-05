from fastapi import Body, FastAPI

# Reading the welcome page:
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Mount the static folder for serving static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/welcomeQwikart", response_class=HTMLResponse)
def root():
     # Get the path of the HTML file
    file_path = os.path.join("templates", "welcome.html")
    
    # Read the HTML file content
    with open(file_path, "r") as file:
        html_content = file.read()
    
    return HTMLResponse(content=html_content)

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

