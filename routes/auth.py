from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from utils.Database import Database

auth = Blueprint('auth', __name__)


@auth.route('/auth')
def Auth():
    return render_template('auth.html')


@auth.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        sproc = "[usr].[UserLogin] @Email = ?, @Password= ?"
        user_email = request.form['email']
        params = (user_email, request.form['password'])
        conn = Database.connect()
        cursor = conn.cursor()
        result = Database.execute_sproc(sproc, params, cursor)

        if "Login successful" == result[0][0]:
            sproc = "[usr].[getUser] @Email = ?"
            params = user_email
            result = Database.execute_sproc(sproc, params, cursor)
            conn.close()
            session['user_id'] = result[0][0]
            session['privilege'] = result[0][1]
            if session['privilege'] in [0, 1]:
                return redirect(url_for('basket.add_item'))
            elif session['privilege'] in [2, 3]:
                return redirect(url_for('admin.Admin'))
        else:
            flash(result[0][0])
    return redirect('/auth')


@auth.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if (int(request.form['accountType']) > 1):
            department_code = 'ST4FF'
        else:
            department_code = request.form['departmentCode']
        if request.form['regPassword'] != request.form['regPassword2']:
            flash('Error: Password does not match')
            return redirect(url_for('auth.Auth'))
        params = (
            request.form['regEmail'],
            request.form['regPassword'],
            request.form['regFirstname'],
            request.form['regLastname'],
            department_code,
            int(request.form['accountType']))

        sproc = """[usr].[CreateUser] @Email = ?, @Password= ?, @FirstName = ?, @LastName = ?, 
        @DepartmentCode = ?, @privileges = ?"""
        conn = Database.connect()
        cursor = conn.cursor()
        info = Database.execute_sproc(sproc, params, cursor)
        cursor.commit()
        conn.close()
        flash(info[0][0])
    return redirect(url_for('auth.Auth'))


@auth.route('/auth/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.Auth'))