# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
from flask import current_app, jsonify

from ..exceptions import (
    EmailAddressTooLong,
    EmptyUserData,
    InvalidEmailAddressFormat,
    MissingEmailData,
    MissingEmailKey,
    MissingNameData,
    MissingNameKey,
    NonDictionaryUserData,
    UserDoesNotExist,
    UserExists,
    UserNameTooLong,
    UserNameTooShort,
)
from ..extensions import db, url_serializer
from ..helpers import check_if_user_exists, check_if_user_with_id_exists, check_if_email_id_match, is_email_address_format_valid
from .helpers import is_user_name_valid
from .models import User, user_schema
from itsdangerous import SignatureExpired, BadTimeSignature


def create_new_user(user_data: dict) -> dict:
    """Create a new user."""
    if not user_data:
        raise EmptyUserData("The user data cannot be empty.")

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData("user_data must be a dict")

    if "Email" not in user_data.keys():
        raise MissingEmailKey("The email is missing from the user data")

    if not user_data["Email"]:
        raise MissingEmailData("The email data is missing")

    if len(user_data["Email"]) >= current_app.config["EMAIL_MAX_LENGTH"]:
        raise EmailAddressTooLong(
            f'The email address should be less than {current_app.config["EMAIL_MAX_LENGTH"]} characters!'
        )

    if not is_email_address_format_valid(user_data["Email"]):
        raise InvalidEmailAddressFormat("The email address is invalid")

    is_user_name_valid(user_data["User Name"])


    if check_if_user_exists(user_data["Email"]):
        raise UserExists(f'The email adress {user_data["Email"]} is already in use.')

    user = User(
        email=user_data["Email"],
        name=user_data["User Name"]
    )

    db.session.add(user)
    db.session.commit()

    return user_schema.dumps(user)


def handle_create_user(request_data: dict):
    """Handle the POST request to the /api/v1/user route."""
    try:
        registered_user_data = create_new_user(request_data)
    except (
        EmptyUserData,
        NonDictionaryUserData,
        MissingEmailKey,
        MissingNameKey,
        EmailAddressTooLong,
        InvalidEmailAddressFormat,
        UserExists,
        MissingEmailData,
        MissingNameData,
        UserNameTooShort,
        UserNameTooLong,
    ) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return registered_user_data, 201
    

def activate_account(email: str):
    """Activate a user account."""
    user = User.query.filter_by(email=email).first()
    user.active = True
    db.session.commit()
    return jsonify({"Email confirmed": email}), 200


def confirm_email(user_id: str, token: str) -> dict:
    """Confrim user account."""
    if not user_id:
        raise ValueError("The user id has to be provided!")
    if not isinstance(user_id, str):
        raise TypeError("The user id has to be a string!")
    if not token:
        raise ValueError("The token has to be provided!")
    if not isinstance(token, str):
        raise TypeError("The token has to be a string!")

    if not check_if_user_with_id_exists(int(user_id)):
        raise UserDoesNotExist(f"The user with id {user_id} does not exist!")

    email = url_serializer.loads(token, salt="somesalt", max_age=60)

    if not check_if_email_id_match(email, int(user_id)):
        raise ValueError(
            f"The id {user_id} and email {email} do not belong to the same user!"
        )

    return activate_account(email)


def handle_email_confirm_request(user_id: str, token: str) -> dict:
    """Handle the GET request to /api/v1/mail/conrfim."""
    try:
        confirm_data = confirm_email(user_id, token)
    except SignatureExpired as e:
        return jsonify({"error": str(e)}), 400
    except BadTimeSignature as e:
        return jsonify({"error": str(e)}), 400
    except (ValueError, TypeError, UserDoesNotExist) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return confirm_data