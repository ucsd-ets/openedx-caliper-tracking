"""
Transformers for all the course settings related events
"""

import json


def edx_course_home_resume_course_clicked(current_event, caliper_event):
    """
    This event is generated when we press the start course button on a course

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    object_extensions = json.loads(current_event['event'])

    object_extensions.update({
        'course_id': current_event['context']['course_id'],
        'org_id': caliper_event['extensions']['extra_fields'].pop('org_id'),
    })

    caliper_object = {
        'id': object_extensions.pop('url'),
        'type': 'CourseSection',
        'extensions': object_extensions
    }

    caliper_event.update({
        'type': 'NavigationEvent',
        'action': 'NavigatedTo',
        'object': caliper_object
    })

    caliper_event['referrer']['type'] = 'WebPage'

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
    })

    return caliper_event


def edx_grades_grading_policy_changed(current_event, caliper_event):
    """
    Event occur while adding grades policy for entrance in course

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_object = {
        'id': current_event['referer'],
        'type': 'CourseOffering',
        'extensions': current_event['event']
    }

    caliper_event.update({
        'type': 'Event',
        'action': 'Modified',
        'object': caliper_object
    })

    caliper_event['referrer']['type'] = 'WebPage'

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['event']['course_id']
    })

    return caliper_event
