import os
from typing import Optional, Dict

from flask import Blueprint, request, render_template, current_app, session, redirect, url_for
from db_work import select_dict
from sql_provider import SQLProvider

blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login:
            user_info = define_user(login, password)
            if user_info:
                user_dict = user_info[0]
                print("USER DICT:", user_dict)
                session['user_id'] = user_dict['user_id']
                if user_dict['user_group']:
                    session['user_group'] = user_dict['user_group']
                else:
                    session['user_group'] = 'external'
                session.permanent = True
                return redirect(url_for('menu_choice'))
            else:
                return render_template('signin.html', message='Пользователь не найден')
        return render_template('signin.html', message='Повторите ввод')


@blueprint_auth.route('/signup', methods=['GET', 'POST'])
def start_reg():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        login = request.form.get('login')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')
        if login:
            if pass1 != pass2:
                return render_template('signup.html', message='Пароли не совпадают')
            user_info = define_user(login, pass1)
            if user_info:
                return render_template('signup.html', message='Пользователь с таким логином уже зарегистрирован')
            registrate_user(login, pass1)
            return redirect('/')
        return render_template('signup.html', message='Повторите ввод')


def define_user(login: str, password: str) -> Optional[Dict]:
    sql_internal = provider.get('internal_user.sql', login=login, password=password)
    sql_external = provider.get('external_user.sql', login=login, password=password)

    user_info = None

    for sql_search in [sql_internal, sql_external]:
        _user_info = select_dict(current_app.config['db_config'], sql_search)
        print('_user_info=', _user_info)
        if _user_info:
            user_info = _user_info
            del _user_info
            break
    return user_info


def registrate_user(login: str, password: str) -> None:
    sql_insert_user = provider.get('register_user.sql', login=login, password=password)
    result = insert(current_app.config['db_config'], sql_insert_user)
    return result