from flask import current_app
from ..exceptions import UserNameTooLong, UserNameTooShort


def is_user_name_valid(user_name: str) -> bool:
    """Check if the user name is valid."""
    if not user_name:
        raise ValueError("The user_name has to be provided.")

    if not isinstance(user_name, str):
        raise ValueError("The user_name has to be string")

    if len(user_name) >= current_app.config["NAME_MAX_LENGTH"]:
        raise UserNameTooLong(
            f'The user_name has to be less than {current_app.config["NAME_MAX_LENGTH"]}'
        )

    if len(user_name) <= current_app.config["NAME_MIN_LENGTH"]:
        raise UserNameTooShort(
            f'The user_name has to be more than {current_app.config["NAME_MIN_LENGTH"]}'
        )

    return True
