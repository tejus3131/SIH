
from flask import render_template

# Custom Module Import

from .administrator import ADMINISTRATOR_URL, ADMINISTRATOR_API
from .student import STUDENT_URL, STUDENT_API
from .university import UNIVERSITY_URL, UNIVERSITY_API
from .authentication import AUTHENTICATION_URL, AUTHENTICATION_API
from .basic import BASIC_URL

class Routes:

    @staticmethod
    def add_routes(app, api):
        app.register_blueprint(BASIC_URL, url_prefix='/')
        app.register_blueprint(ADMINISTRATOR_URL, url_prefix='/administrator')
        app.register_blueprint(STUDENT_URL, url_prefix='/student')
        app.register_blueprint(UNIVERSITY_URL, url_prefix='/university')
        app.register_blueprint(AUTHENTICATION_URL, url_prefix='/authentication')
        for route in AUTHENTICATION_API + ADMINISTRATOR_API + STUDENT_API + UNIVERSITY_API:
            api.add_resource(route[2], route[0], endpoint=route[1])

        @app.errorhandler(404)
        def page_not_found(e):
            return render_template("404.html")

        @app.errorhandler(500)
        def internal_error(e):
            return render_template("500.html")