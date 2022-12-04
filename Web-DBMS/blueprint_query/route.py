import os

from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider
from access import group_required

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/queries_1', methods=['GET', 'POST'])
@group_required
def queries_1():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
            _sql = provider.get('product.sql', input_product=input_product)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return 'repeat input'

@blueprint_query.route('/queries_2', methods=['GET', 'POST'])
@group_required
def queries_2():
    if request.method == 'GET':
        return render_template('category_form.html')
    else:
        input_prod_category = request.form.get('input_prod_category')
        if input_prod_category:
            _sql = provider.get('cost.sql', input_prod_category=input_prod_category)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('category_result.html', schema=schema, result=product_result)
        else:
            return render_template('category_form.html', message="Данные не найдены")