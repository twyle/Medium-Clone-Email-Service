from ..auth.models import User


def check_if_user_active(id: int) -> bool:
    """Check if account has been activated."""
    return User.query.filter_by(id=id).first().active