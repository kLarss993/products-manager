from flask import Flask, request, redirect, flash, render_template
from actions_db import *
import models

app = Flask(__name__)
app.secret_key = 'key'
models.init_db()


@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def index():
    selected_category = request.args.get('category', 'all')

    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')

        if product_exists(name):
            flash('Такий товар вже є!')
        else:
            add_product(name, price, category)
            flash('Товар додано!')

        return redirect('/')

    if selected_category == 'all':
        filtered_products = get_all_products()
    else:
        filtered_products = get_product_by_category(selected_category)

    categories = get_all_categories()

    return render_template(
        'index.html',
        products=filtered_products,
        categories=categories,
        selected_category=selected_category
    )


@app.route('/delete/<name>')
def delete(name):
    if product_exists(name):
        delete_product(name)
        flash(f'Товар {name} видалено!')
    else:
        flash('Товар не знайдено!')

    return redirect('/')


@app.route('/edit/<product_name>', methods=['GET', 'POST'])
def update(product_name):
    product = Product.get_or_none(Product.name == product_name)

    if request.method == 'POST':
        price = request.form.get('price')
        category = request.form.get('category')

        update_product(price, category)

        flash("Товар оновлено")
        return redirect('/')

    return render_template(
        'update.html',
        product=product
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
