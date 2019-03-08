"""
Transformers for all the xblock events
"""


def xblock_poll_view_results(current_event, caliper_event):
    """
    The server emits an xblock.poll.view_results event when
    a tally of the responses to a poll is displayed to a user.
    For a poll that has the Private Results option set to False,
    the tally appears after a user submits a response.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'Result'
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


def xblock_survey_view_results(current_event, caliper_event):
    """
    The server emits an xblock.survey.view_results event
    when a matrix of survey response percentages is displayed
    to a user. For surveys that have the Private Results option set
    to False only, the matrix appears after a user submits survey responses.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'Result',
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


def xblock_survey_submitted(current_event, caliper_event):
    """
    The server emits an xblock.survey.submitted event each
    time a user submits responses to a survey.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'Assessment',
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
        'type': 'AssessmentEvent',
        'action': 'Submitted',
        'object': caliper_object
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def xblock_poll_submitted(current_event, caliper_event):
    """
    The server emits an xblock.poll.submitted event each
    time a user submits a response to a poll.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'Assessment',
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
        'type': 'AssessmentEvent',
        'action': 'Submitted',
        'object': caliper_object
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def xblock_split_test_child_render(current_event, caliper_event):
    """
    When a student views a module that is set up to test different
    content using child modules, the server emits a xblock.split_test.child_render
    event to identify the child module that was shown to the student.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'type': 'DigitalResource',
        'extensions': current_event['event']
    }
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id'],
        'module': current_event['context']['module'],
        'course_user_tags': current_event['context']['course_user_tags'],
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
