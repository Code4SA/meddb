from flask import render_template
from frontend import app
import requests

api_host = app.config['API_HOST']

@app.route('/')
def root():

    return render_template('index.html', active_nav_button="home")


@app.route('/medicine/')
def medicine_index():

    response = requests.get(api_host + 'medicine/')
    medicine_list = response.json()
    return render_template('medicine_index.html', medicine_list=medicine_list, active_nav_button="medicines")


@app.route('/medicine/<medicine_id>/')
def medicine(medicine_id):

    response = requests.get(api_host + 'medicine/' + str(medicine_id) + "/")
    medicine = response.json()
    return render_template('medicine.html', medicine=medicine, active_nav_button="medicines")


@app.route('/product/<product_id>/')
def product(product_id):

    response = requests.get(api_host + 'product/' + str(product_id) + "/")
    product = response.json()
    return render_template('product.html', product=product, active_nav_button="medicines")


@app.route('/supplier/')
def supplier_index():

    response = requests.get(api_host + 'supplier/')
    supplier_list = response.json()
    return render_template('supplier_index.html', supplier_list=supplier_list, active_nav_button="suppliers")


@app.route('/supplier/<supplier_id>/')
def supplier(supplier_id):

    response = requests.get(api_host + 'supplier/' + str(supplier_id) + "/")
    supplier = response.json()
    return render_template('supplier.html', supplier=supplier, active_nav_button="suppliers")