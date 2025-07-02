from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML pages
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/products", response_class=HTMLResponse)
async def read_products_page():
    with open("products.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/order", response_class=HTMLResponse)
async def read_order_page():
    with open("order.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/contact", response_class=HTMLResponse)
async def read_contact_page():

@app.post("/api/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=order.product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.create_order(db=db, order=order)

@app.get("/api/orders", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders
    with open("contact.html") as f:
        return HTMLResponse(content=f.read())

# API Endpoints

@app.get("/api/products", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

# Need to add endpoint for creating orders later
# Need to add endpoint for creating products (admin)
