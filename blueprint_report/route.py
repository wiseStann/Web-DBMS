import os
from flask import render_template, request, Blueprint, redirect, url_for, current_app
from db_work import call_proc, select, select_dict
from sql_provider import SQLProvider
from access import group_required, login_required

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET', 'POST'])
@login_required
@group_required
def start_report():
    report_url = current_app.config['report_url']
    report_list = current_app.config['report_list']
    if request.method == 'GET':
        return render_template('menu_report.html', report_list=report_list, endcoding='UTF-8')
    else:
        if 'back-button' in request.form.keys():
            return redirect('/services')
        rep_id = request.form.get('rep_id')
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        return redirect(url_for(url_rep))


@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        if 'back-button' in request.form.keys():
            return redirect(url_for('bp_report.start_report'))
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        if input_year and input_month:
            _sql = provider.get('info_of_sale.sql', input_year=input_year, input_month=input_month)
            info_result = select_dict(current_app.config['db_config'], _sql)
            if len(info_result) == 0:
                return render_template('report_create.html', error_message='Продаж в этом месяце не было')
            else:
                _sql = provider.get('summa_price.sql', input_month=input_month, input_year=input_year)
                product_result = select_dict(current_app.config['db_config'], _sql)
                if len(product_result) != 0:
                    return render_template('report_create.html', error_message='Отчет уже существует')
                else:
                    res = call_proc(current_app.config['db_config'], 'create_product_report', int(input_month), int(input_year))
                    print('res = ', res)
                    return render_template('report_create.html', success_message='Отчет создан!')
        else:
            return render_template('report_create.html', error_message='Повторите ввод')


@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        if 'back-button' in request.form.keys():
            return redirect(url_for('bp_report.start_report'))
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        print(input_year)
        print(input_month)
        if input_year and input_month:
            _sql = provider.get('info_of_sale.sql', input_year=input_year, input_month=input_month)
            info_result = select_dict(current_app.config['db_config'], _sql)
            if len(info_result) == 0:
                return render_template('report_create.html', error_message='Продаж в этом месяце не было')
            else:
                _sql = provider.get('summa_price.sql', input_month=input_month, input_year=input_year)
                product_result, schema = select(current_app.config['db_config'], _sql)

                if len(product_result) == 0:
                    return render_template('report_create.html', error_message='Отчета не найдено')
                else:
                    list_name=['ID товара', 'Продано единиц', 'Месяц создания отчета', 'Год создания отчета']
                    return render_template('report_result.html', schema=list_name, result=product_result)
        else:
            return render_template('report_create.html', error_message='Повторите ввод')


@blueprint_report.route('/create_rep2', methods=['GET', 'POST'])
@group_required
def create_rep2():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        if 'back-button' in request.form.keys():
            return redirect(url_for('bp_report.start_report'))
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        if input_year and input_month:
            _sql = provider.get('info_of_sale.sql', input_year=input_year, input_month=input_month)
            info_result = select_dict(current_app.config['db_config'], _sql)
            if len(info_result) == 0:
                return render_template('report_create.html', error_message='Продаж в этом месяце не было')
            else:
                _sql = provider.get('summa_price.sql', input_month=input_month, input_year=input_year)
                product_result = select_dict(current_app.config['db_config'], _sql)
                if len(product_result) != 0:
                    return render_template('report_create.html', error_message='Отчет уже существует')
                else:
                    res = call_proc(current_app.config['db_config'], 'create_product_report', int(input_month), int(input_year))
                    print('res = ', res)
                    return render_template('report_create.html', success_message='Отчет создан!')
        else:
            return render_template('report_create.html', error_message='Повторите ввод')


@blueprint_report.route('/view_rep2', methods=['GET', 'POST'])
@group_required
def view_rep2():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        if 'back-button' in request.form.keys():
            return redirect(url_for('bp_report.start_report'))
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        print(input_year)
        print(input_month)
        if input_year and input_month:
            _sql = provider.get('info_of_sale.sql', input_year=input_year, input_month=input_month)
            info_result = select_dict(current_app.config['db_config'], _sql)
            if len(info_result) == 0:
                return render_template('report_create.html', error_message='Продаж в этом месяце не было')
            else:
                _sql = provider.get('summa_price.sql', input_month=input_month, input_year=input_year)
                product_result, schema = select(current_app.config['db_config'], _sql)

                if len(product_result) == 0:
                    return render_template('report_create.html', error_message='Отчета не найдено')
                else:
                    list_name=['Сумма', 'Количество проданных товаров', 'Месяц создание отчета', 'Год создания отчета']
                    return render_template('report_result.html', schema=list_name, result=product_result)
        else:
            return render_template('report_create.html', error_message='Повторите ввод')
 