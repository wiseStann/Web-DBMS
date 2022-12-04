import os.path

from flask import *
from db_work import select_dict
from sql_provider import SQLProvider
from db_context_manager import DBContextManager


blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route('/', methods=['GET', 'POST'])
def order_index():
    db_config = current_app.config['db_config']
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)
        basket_items = session.get('basket', {})
        return render_template('basket_order_list.html', items=items, basket=basket_items)
    else:
        prod_id = request.form['prod_id']
        sql = provider.get('all_items.sql', prod_id=prod_id)
        items = select_dict(db_config, sql)
        print('items:', items)
        # сделать новый sql, который достает только новый item
        add_to_basket(prod_id, items)
        return redirect(url_for('bp_order.order_index'))


def add_to_basket(prod_id: str, items: dict):
    curr_basket = session.get('basket', {})
    if prod_id in curr_basket:
        curr_basket[prod_id]['prod_amount'] = curr_basket[prod_id]['prod_amount'] + 1
    else:
        curr_basket[prod_id] = {
            'prod_name' : items[0]['prod_name'],
            'prod_price' : items[0]['prod_price'],
            'prod_amount' : 1
        }
        session['basket'] = curr_basket
        session.permanent = True
    return True


@blueprint_order.route('/save_order', methods=['GET', 'POST'])
def save_order():
    user_id = session.get('user_id')
    current_basket = session.get('basket', {})
    order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket)
    if order_id:
        session.pop('basket') #очищает сессию по ключу
        return render_template('order_created.html', order_id=order_id)
    else:
        return "Smth went wrong"


def save_order_with_list(dbconfig: dict, user_id: int, current_basket: dict):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        _sql1 = provider.get('insert_order.sql', user_id=user_id)
        result1 = cursor.execute(_sql1)
        print(result1)
        if result1 == 1:
            _sql2 = provider.get('select_order_id.sql', user_id=user_id)
            cursor.execute(_sql2)
            order_id = cursor.fetchall()[0][0]
            print('order_id = ', order_id)
            if order_id:
                for key in current_basket:
                    print(key, current_basket[key]['prod_amount'])
                    prod_amount = current_basket[key]['prod_amount']
                    _sql3 = provider.get('insert_order_list.sql', order_id=order_id, prod_id=key, prod_amount=prod_amount)
                    cursor.execute(_sql3)
                return order_id


@blueprint_order.route('/clear_basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_order.order_index'))