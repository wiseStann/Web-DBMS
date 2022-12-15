import os

from flask import Blueprint, request, render_template, current_app, redirect, url_for
from db_work import select
from sql_provider import SQLProvider
from access import group_required

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/menu', methods=['GET', 'POST'])
@group_required
def queries():
    if request.method == 'GET':
        return render_template('queries.html')
    else:
        return redirect('/services')


@blueprint_query.route('/query1', methods=['GET', 'POST'])
@group_required
def query_1():
    if request.method == 'GET':
        return render_template('product_query.html')
    else:
        if 'back-button' in request.form.keys():
            return redirect(url_for('bp_query.queries'))
        input_product = request.form.get('product_name')
        if input_product:
            input_product = request.form.get('product_name')
            _sql = provider.get('product.sql', input_product=input_product)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('query_result.html', schema=schema, result=product_result)
        return render_template('product_query.html')


@blueprint_query.route('/query2', methods=['GET', 'POST'])
@group_required
def query_2():
    if request.method == 'GET':
        return render_template('category_query.html')
    else:
        if 'back-button' in request.form.keys():
            return redirect(url_for('bp_query.queries'))
        input_prod_category = request.form.get('input_prod_category')
        if input_prod_category:
            _sql = provider.get('cost.sql', input_prod_category=input_prod_category)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('query_result.html', schema=schema, result=product_result)
        else:
            return redirect(url_for('bp_query.queries'))
