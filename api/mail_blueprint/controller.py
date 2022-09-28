from flask import jsonify
from ..helpers import (
    is_email_address_format_valid, 
    check_if_user_with_id_exists,
    check_if_user_exists,
    check_if_email_id_match
)
from ..exceptions import UserDoesNotExist, ActivatedAccount
from .helpers import check_if_user_active
from ..tasks import celery_send_email


def send_confirm_email(user_id: str, email_data: dict) -> dict:
    """Send account confirmation email."""
    if not user_id:
        raise ValueError("The user id must be provided")
    if not isinstance(user_id, str):
        raise TypeError("The user id must be a string")
    if not email_data:
        raise ValueError("The email data cannot be empty")
    if not isinstance(email_data, dict):
        raise TypeError("The email data should be a dict")
    if "email" not in email_data.keys():
        raise ValueError("The email key is missing in email data")
    if not email_data["email"]:
        raise ValueError("The email cannot be empty")
    if not is_email_address_format_valid(email_data["email"]):
        raise ValueError("The email address format is invalid")
    if not check_if_user_with_id_exists(int(user_id)):
        raise UserDoesNotExist(f"The user with id {user_id} does not exist!")
    if not check_if_user_exists(email_data["email"]):
        raise UserDoesNotExist(
            f'The user with email {email_data["email"]} does not exist!'
        )

    if not check_if_email_id_match(email_data["email"], int(user_id)):
        raise UserDoesNotExist(
            f'There is no user with the id {user_id} and email {email_data["email"]}'
        )

    if check_if_user_active(int(user_id)):
        raise ActivatedAccount("This account has alreadybeen activated!")

    task = celery_send_email.delay(
        user_id, email_data["email"], "Confirm Account", "auth.confirm_email"
    )

    return (
        jsonify(
            {"task_id": task.id, "Confirm Account email sent to": email_data["email"]}
        ),
        202,
    )
    

def handle_send_confirm_email(user_id: str, email_data: dict) -> dict:
    """Send the confirmation email."""
    try:
        confirm_email_data = send_confirm_email(user_id, email_data)
    except (ValueError, TypeError, UserDoesNotExist, ActivatedAccount) as e:
        return jsonify({"error": str(e)})
    else:
        return confirm_email_data