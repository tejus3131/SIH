from flask import Blueprint, request
from flask_restful import Resource

from ..services.authentication import AuthenticationManager

ADMINISTRATOR_API = [
]

ADMINISTRATOR_URL = Blueprint('administrator', __name__)

@ADMINISTRATOR_URL.route('/')
@AuthenticationManager.administrator_required
def home():
    return 'Administrator Home'