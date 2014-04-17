from flask import render_template
from frontend import app
import requests
import dateutil.parser
import operator

api_host = app.config['API_HOST']


def sort_list(unsorted_list, key):
    """
    Sort a list of dicts by the value found with the key provided.
    """

    return sorted(unsorted_list, key=operator.itemgetter(key))


@app.template_filter('format_date')
def jinja2_filter_format_date(date_str):
    date = dateutil.parser.parse(date_str)
    native = date.replace(tzinfo=None)
    format='%b %Y'
    return native.strftime(format)

@app.route('/')
def root():

    return render_template('index.html', active_nav_button="home")


@app.route('/medicine/')
def medicine_index():

    response = requests.get(api_host + 'medicine/')
    medicine_list = sort_list(response.json(), 'name')
    return render_template('medicine_index.html', medicine_list=medicine_list, active_nav_button="medicines")


@app.route('/medicine/<medicine_id>/')
def medicine(medicine_id):

    response = requests.get(api_host + 'medicine/' + str(medicine_id) + "/")
    medicine = response.json()

    tmp = {}
    if medicine.get('procurements'):
        for i in range(len(medicine['procurements'])):
            procurement = medicine['procurements'][i]
            packing = str(procurement['container']['quantity']) + " " + str(procurement['container']['unit']) + " " + procurement['container']['type']
            key = str(procurement['country']['name'] + " - " + packing)
            if not tmp.get(key):
                tmp[key] = {'avg_price': procurement['price_per_unit'], 'total_units': procurement['container']['quantity'] * procurement['volume']}
            else:
                total_price = tmp[key]['avg_price'] * tmp[key]['total_units']
                total_price += (procurement['price_per_unit'] * procurement['container']['quantity'] * procurement['volume'])
                tmp[key]['total_units'] += procurement['container']['quantity'] * procurement['volume']
                tmp[key]['avg_price'] = total_price / tmp[key]['total_units']

    # convert to a list, then sort
    tmp_list = []
    for key, val in tmp.iteritems():
        val['label'] = key
        tmp_list.append(val)
    tmp_list = sort_list(tmp_list, 'avg_price')
    tmp_list.reverse()

    max_price = medicine['mshprice']
    graph_data = []
    labels = []
    i = 0
    for entry in tmp_list:
        graph_data.append([entry['avg_price'], i])
        labels.append([i, entry['label']])
        if entry['avg_price'] > max_price:
            max_price = entry['avg_price']
        i += 1

    return render_template('medicine.html',
                           medicine=medicine,
                           active_nav_button="medicines",
                           graph_data=graph_data,
                           labels=labels,
                           max_price=max_price)


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


@app.route('/procurement/<procurement_id>/')
def procurement(procurement_id):

    response = requests.get(api_host + 'procurement/' + str(procurement_id) + "/")
    procurement = response.json()
    return render_template('procurement.html', procurement=procurement)