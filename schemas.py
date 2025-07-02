from pydantic import BaseModel

class OrderBase(BaseModel):
    product_id: int
    quantity: int
    customer_name: str
    customer_email: str
    shipping_address: str

class Order(OrderBase):
    pass

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    image_url: str | None = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True