"""
This module contains helper methods used by the app.
"""
from eventtracking import tracker


def emit_login_event(*args, **kwargs):
    """
    Server emits event when user is logged in through third party authentication app.
    """
    user = kwargs['user']
    event_name = 'edx.user.login'
    event_data = {
        'email': user.email,
        'username': user.username,
        'user_id': user.id,
        'is_new': kwargs['is_new'],
        'new_association': kwargs['new_association'],
        'verified': kwargs['response'].get('verified')
    }
    tracker.emit(event_name, event_data)
