from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .controller import (
    handle_create_user,
    handle_email_confirm_request,
)


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
@swag_from("./docs/register_user.yml", endpoint="auth.register", methods=["POST"])
def register():
    """Create a new User."""
    return handle_create_user(request.form)


@auth.route('/confirm', methods=['GET'])
@swag_from("./docs/confirm.yml", endpoint='auth.confirm_email', methods=['GET'])
def confirm_email():
    """Handle email confirmation."""
    return handle_email_confirm_request(request.args.get('id'), request.args.get('token'))