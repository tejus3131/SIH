from flask import Blueprint, render_template


def display_page(
    page: str,
    args: dict | None = {},
    nav: bool | None = True,
    footer: bool | None = True
):
    return render_template(
        page,
        args=args,
        nav=nav,
        footer=footer
    )


BASIC_URL = Blueprint('basic', __name__)


@BASIC_URL.route('/')
def index():
    return display_page('landing_page.html')
