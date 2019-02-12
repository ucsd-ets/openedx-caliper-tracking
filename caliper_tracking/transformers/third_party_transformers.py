"""
Transformers for all the Third-Party events
"""


def edx_googlecomponent_calendar_displayed(current_event, caliper_event):
    """
    The server emits an edx.googlecomponent.calendar.displayed
    event when a Google Calendar component is shown in the LMS.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'Frame',
        'extensions': current_event['event']
    }
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id'],
        'module': current_event['context']['module'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'asides': current_event['context']['asides']
    })
    caliper_event.update({
        'type': 'ViewEvent',
        'action': 'Viewed',
        'object': caliper_object
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def edx_googlecomponent_document_displayed(current_event, caliper_event):
    """
    The server emits an edx.googlecomponent.document.displayed
    event when a Google Drive file, such as a document,
    spreadsheet, or image, is shown in the LMS.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'Document',
        'extensions': current_event['event']
    }
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id'],
        'module': current_event['context']['module'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'asides': current_event['context']['asides']
    })
    caliper_event.update({
        'type': 'ViewEvent',
        'action': 'Viewed',
        'object': caliper_object
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def oppia_exploration_state_changed(current_event, caliper_event):
    """
    The server emits an oppia.exploration.state.changed event when
    a user interacts with an Oppia exploration component by submitting
    an answer. Answers are not incorrect or correct.
    All answer submissions change the state of the exploration.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'AssessmentItem',
        'extensions': current_event['event']
    }
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id'],
        'module': current_event['context']['module'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'asides': current_event['context']['asides']
    })
    caliper_event.update({
        'type': 'Event',
        'action': 'Modified',
        'object': caliper_object
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def oppia_exploration_loaded(current_event, caliper_event):
    """
    The server emits an oppia.exploration.loaded event
    when an Oppia exploration component is shown in the LMS.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'AssessmentItem',
        'extensions': current_event['event']
    }
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id'],
        'module': current_event['context']['module'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'asides': current_event['context']['asides']
    })
    caliper_event.update({
        'type': 'Event',
        'action': 'Started',
        'object': caliper_object
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def oppia_exploration_completed(current_event, caliper_event):
    """
    The server emits an oppia.exploration.completed event when
    a user completes an interaction with an Oppia exploration component.
    Oppia explorations do not emit grading events.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'AssessmentItem',
        'extensions': current_event['event']
    }
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id'],
        'module': current_event['context']['module'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'asides': current_event['context']['asides']
    })
    caliper_event.update({
        'type': 'Event',
        'action': 'Completed',
        'object': caliper_object
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event
