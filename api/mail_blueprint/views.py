from flask import Blueprint, request
from .controller import handle_send_confirm_email
from flasgger import swag_from


mail = Blueprint('mail', __name__)

@mail.route('/send', methods=['POST'])
@swag_from("./docs/send.yml", endpoint='mail.send_mail', methods=['POST'])
def send_mail():
    """Send an email"""
    return handle_send_confirm_email(request.args.get("id"), request.json)
