from flask import Blueprint
from ..services.authentication import AuthenticationManager

from flask_restful import Resource

UNIVERSITY_API = []

UNIVERSITY_URL = Blueprint('university', __name__)

@UNIVERSITY_URL.route('/')
@AuthenticationManager.university_required
def home():
    return 'University Home'