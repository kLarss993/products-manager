from models import Product

# отримання
def get_all_products():
    return Product.select()

def get_product_by_category(category: str):
    return Product.select().where(Product.category == category)

def product_exists(name: str) -> bool:
    return Product.select().where(Product.name == name).exists()

def get_all_categories():
    return Product.select(Product.category).distinct().order_by(Product.category)

# додавання
def add_product(name: str, price: float, category: str):
    Product.create(name=name, price=price, category=category)

# видалення
def delete_product(name: str):
    Product.delete().where(Product.name == name).execute()


def update_product(price: float, category: str):
        Product.update(price=price,category=category).where(Product.name == Product.name).execute()
