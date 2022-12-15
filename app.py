from flask import Flask, request, url_for, render_template, json, session, redirect

from blueprint_auth.route import blueprint_auth
from blueprint_query.route import blueprint_query
from blueprint_basket.route import blueprint_order
from blueprint_report.route import blueprint_report

from access import login_required, group_required

app = Flask(__name__)
app.secret_key = 'Superley'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/queries')
app.register_blueprint(blueprint_order, url_prefix='/order')
app.register_blueprint(blueprint_report, url_prefix='/report')

app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))
app.config['report_list'] = json.load(open('data_files/report_list.json', encoding='UTF-8'))
app.config['report_url'] = json.load(open('data_files/report_url.json', encoding='UTF-8'))


@app.route('/', methods=['GET', 'POST'])
def menu_choice():
    if 'user_id' in session:
        return render_template('base.html', base=True, auth=True)
    else:
        return render_template('base.html', base=True, auth=False)

@app.route('/services', methods=['GET', 'POST'])
@login_required
@group_required
def services():
    if request.method == 'GET':
        if session.get('user_group') == 'external':
            return render_template('external_user_menu.html')
        is_admin = (session.get('user_group') == 'admin')
        return render_template('internal_user_menu.html', admin=is_admin)
    else:
        return redirect('/')

@app.route('/exit')
def exit_func():
    if 'user_id' in session:
        session.pop('user_id')
    if 'user_group' in session:
        session.pop('user_group')
    return redirect(url_for('menu_choice'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500)
