from flask import Blueprint, render_template, request, redirect, url_for
from flask_restful import Resource

from ..services.database import DatabaseManager
from ..services.authentication import AuthenticationManager
from .basic import display_page


class Administrator(Resource):
    def post(self):
        data = request.form
        username = data.get('username')
        password = data.get('password')
        return AuthenticationManager.login_administrator(username=username, password=password)


class University(Resource):
    def post(self):
        data = request.form
        username = data.get('username')
        password = data.get('password')
        return AuthenticationManager.login_university(username=username, password=password)


AUTHENTICATION_API = [
    ('/validate/administrator/', 'administrator', Administrator),
    ('/validate/university/', 'university', University)
]

AUTHENTICATION_URL = Blueprint('authentication', __name__)


@AUTHENTICATION_URL.route('/student/')
def student():
    return display_page('authentication.html', args={
        'universities': DatabaseManager.get_all_universities()},
        nav=False, footer=False)


@AUTHENTICATION_URL.route('/administrator/')
def administrator():
    return display_page('authentication.html', args={
        'type': 'administrator',
        'api': '/validate/administrator/',
        'redirect': '/administrator/'},
        nav=False, footer=False)


@AUTHENTICATION_URL.route('/university/')
def university():
    return display_page('authentication.html', args={
        'type': 'university',
        'api': '/validate/university/',
        'redirect': '/university/'},
        nav=False, footer=False)


@AUTHENTICATION_URL.route('/logout/')
def logout():
    AuthenticationManager.logout()
    return redirect(url_for('basic.index'))
