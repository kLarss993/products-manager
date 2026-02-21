from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, redirect, flash, render_template, url_for, session
from actions_db import *
import models, re

app = Flask(__name__)
app.secret_key = 'key'
models.init_db()


def is_logged():
    return 'company_name' in session


def current_company():
    if 'company_name' not in session:
        return None
    return get_company_by_name(session['company_name'])


@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def index():
    if not is_logged():
        return redirect(url_for('login'))

    selected_category = request.args.get('category', 'all')

    company = current_company()

    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')

        if product_exists(company.id, name):
            flash('Такий товар вже є!')
        else:
            add_product(company_id, name, price, category)
            flash('Товар додано!')

        return redirect('/')

    if selected_category == 'all':
        filtered_products = get_all_products(company.id)
    else:
        filtered_products = get_product_by_category(company.id, selected_category)

    categories = get_all_categories(company.id)

    return render_template(
        'index.html',
        products=filtered_products,
        categories=categories,
        selected_category=selected_category
    )


@app.route('/delete/<name>')
def delete(name):
    if not is_logged():
        return redirect(url_for('login'))

    company = current_company()

    if product_exists(company.id, name):
        delete_product(name)
        flash(f'Товар {name} видалено!')
    else:
        flash('Товар не знайдено!')

    return redirect('/')


@app.route('/edit/<product_name>', methods=['GET', 'POST'])
def update(product_name):
    if not is_logged():
        return redirect(url_for('login'))

    company = current_company()
    product = Product.get_or_none(Product.name == product_name)

    if request.method == 'POST':
        price = request.form.get('price')
        category = request.form.get('category')

        update_product(company.id, price, category)

        flash("Товар оновлено")
        return redirect('/')

    return render_template(
        'update.html',
        product=product
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name_company = request.form.get('name')
        password = request.form.get('password')

        if not name_company:
            flash("Логін не може бути порожнім")
            return redirect("/register")

        if len(password) < 6:
            flash("Пароль має містити мінімум 6 символів")
            return redirect("/register")

        if not re.search(r"[A-Za-zА-Яа-яІіЇїЄєҐґ]", password):
            flash("Пароль має містити хоча б одну літеру")
            return redirect("/register")

        if company_exists(name_company):
            flash(f'Компанія {name_company} вже існує')
            return redirect(url_for('register'))

        heshed_password = generate_password_hash(password)

        add_company(name_company, heshed_password)
        flash(f'Компанія {name_company} створена')
        return redirect(url_for('login'))


    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name_company = request.form.get('name')
        password = request.form.get('password')

        if not company_exists(name_company):
            flash(f'Company {name_company} not exists!')
            return redirect(url_for('login'))

        company = get_company_by_name(name_company)
        if not check_password_hash(company.password, password):
            flash('Password incorrect!')
            return redirect(url_for('login'))

        session['company_name'] = company.name
        flash('Ви війшли в сисетму')
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('company_name')
    flash('Ви вийшли з системи')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
