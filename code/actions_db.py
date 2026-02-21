from models import Product, Company

# отримання
def get_all_products(company_id: int):
    return Product.select().where(Product.company == company_id)

def get_product_by_category(category: str, company_id: int):
    return Product.select().where((Product.category == category) & (Product.company == company_id))

def product_exists(name: str, company_id: int) -> bool:
    return Product.select().where((Product.name == name) & (Product.company == company_id)).exists()

def get_all_categories(company_id: int):
    return Product.select(Product.category).where(Product.company == company_id).distinct().order_by(Product.category)

# додавання
def add_product(name: str, price: float, category: str, company_id: int):
    Product.create(name=name, price=price, category=category, company=company_id)

# видалення
def delete_product(name: str, company_id: int):
    Product.delete().where((Product.name == name) & (Product.company == company_id)).execute()


def update_product(price: float, category: str, company_id: int):
    Product.update(price=price,category=category).where((Product.name == Product.name) & (Product.company == company_id)).execute()




def add_company(name_company: str, password: str):
    Company.create(name=name_company, password=password)


def company_exists(company_name: str):
    return Company.select().where(Company.name == company_name).exists()

def get_company_by_name(name_company: str):
    return Company.get_or_none(Company.name == name_company)