
# In-built Module Import

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, flash, redirect, url_for, jsonify
import requests

# Custom Module Import

from .database import DatabaseManager



class User(UserMixin):
    def __init__(self, id):
        self.id = id


class AuthenticationManager:

    @staticmethod
    def login_required(func):
        def check_login(*args, **kwargs):
            if 'logged_in' not in session:
                flash('Please login to access this page.', 'danger')
                return redirect(url_for('authentication.student'))
            return func(*args, **kwargs)
        check_login.__name__ = func.__name__
        return check_login

    @staticmethod
    def university_required(func):
        def check_university(*args, **kwargs):
            if 'logged_in' not in session:
                flash(
                    'Please login from a University account to access this page.', 'danger')
                return redirect(url_for('authentication.university'))
            if session['privilege'] != 'university':
                flash('Only universitys can access this page.', 'danger')
                if session['privilege'] == 'administrator':
                    return redirect(url_for('administrator.page'))
                else:
                    return redirect(url_for('student.page'))
            return func(*args, **kwargs)
        check_university.__name__ = func.__name__
        return check_university

    @staticmethod
    def administrator_required(func):
        def check_administrator(*args, **kwargs):
            if 'logged_in' not in session:
                flash(
                    'Please login as a administrator to access this page.', 'danger')
                return redirect(url_for('authentication.administrator'))
            elif session['privilege'] != 'administrative':
                flash('Only administrator can access this page', 'danger')
                if session['privilege'] == 'university':
                    return redirect(url_for('university.page'))
                else:
                    return redirect(url_for('student.page'))
            elif not DatabaseManager.check_administrator(session['uid']):
                flash("Only administrators can access these routes.", "danger")
                return redirect(url_for('views.home'))
            return func(*args, **kwargs)
        check_administrator.__name__ = func.__name__
        return check_administrator

    # @staticmethod
    # def login_student(university: str, credentials: tuple):
    #     query = {
    #         '$and': [
    #             {'university': 'desired_university'},
    #             {'username': 'desired_username'}
    #         ]
    #     }
        # user = users.find_one(query)
        # if user:
        #     if check_password_hash(user['password'], password):
        #         session['logged_in'] = True
        #         session['_id'] = email
        #         if email in admins or user['admin'] == True:
        #             session['admin'] = True
        #         else:
        #             session['admin'] = user['admin']
        #         return jsonify({'message': 'success'})
        #     else:
        #         return jsonify({'message': 'Incorrect password'})
        # else:
        #     return jsonify({'message': 'User does not exist'})

    @staticmethod
    def login_administrator(username: str, password: str):
        status, result = DatabaseManager()._instance.verify_administrator(username=username, password=password)
        if not status:
            response = {
                'status': False,
                'message': result
            }
            return response, 401
        
        session['logged_in'] = True
        session['privilege'] = 'administrative'
        session['uid'] = result['_id']

        response = {
            'status': True,
            'route': url_for('administrator.home')
        }

        return response, 200
    
    @staticmethod
    def login_university(username: str, password: str):
        status, result = DatabaseManager()._instance.verify_university(username=username, password=password)
        if not status:
            response = {
                'status': False,
                'message': result
            }
            return response, 401
        
        session['logged_in'] = True
        session['privilege'] = 'university'
        session['uid'] = result['_id']

        response = {
            'status': True,
            'route': url_for('university.home')
        }

        return response, 200


    @staticmethod
    def register():
        # email = request.form.get('registerEmail')
        # password = request.form.get('registerPassword')
        # confirm_password = request.form.get('registerRepeatPassword')

        # if password != confirm_password:
        #     return jsonify({'message': 'Passwords do not match'})
        # if users.find_one({'_id': email}):
        #     return jsonify({'message': 'User already exists'})
        # hashed_password = generate_password_hash(password, method='scrypt')
        # admin = False
        # if email in admins:
        #     admin = True
        # users.insert_one({
        #     '_id': email,
        #     'password': hashed_password,
        #     'courses': [],
        #     'admin': admin,
        # })
        # session['logged_in'] = True
        # session['_id'] = email
        # session['admin'] = admin
        # return jsonify({'message': 'success'})
        pass

    @staticmethod
    def logout():
        session.clear()
