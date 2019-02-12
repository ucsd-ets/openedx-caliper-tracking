"""
Transformers for all the video events
"""

import json
from datetime import timedelta

from isodate import duration_isoformat


def pause_video(current_event, caliper_event):
    """
    When a user selects the video player's pause control,
    the player emits a pause_video event. For videos that
    are streamed in a browser, when the player reaches the
    end of the video file and play automatically stops it
    emits both this event and a stop event (as of June 2014).

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    current_event_details = json.loads(current_event['event'])
    caliper_event.update({
        'action': 'Paused',
        'type': 'MediaEvent',
        'object': {
            'duration': duration_isoformat(timedelta(
                seconds=current_event_details['duration']
            )),
            'extensions': {
                'code': current_event_details['code'],
                'id': current_event_details['id']
            },
            'id': current_event['referer'],
            'type': 'VideoObject'
        },
        'target': {
            'currentTime': duration_isoformat(timedelta(
                seconds=current_event_details['currentTime']
            )),
            'id': current_event['referer'],
            'type': 'MediaLocation'
        }
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def stop_video(current_event, caliper_event):
    """
    When the video player reaches the end of the video file and play
    automatically stops, the player emits a stop_video event.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    current_event_details = json.loads(current_event['event'])
    caliper_object = {
        'id': current_event['referer'],
        'type': 'VideoObject',
        'duration': duration_isoformat(
            timedelta(seconds=current_event_details['duration'])
        ),
        'extensions': {
            'code': current_event_details['code'],
            'id': current_event_details['id']
        }
    }
    caliper_event.update({
        'type': 'MediaEvent',
        'action': 'Ended',
        'object': caliper_object,
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })
    return caliper_event


def edx_video_speed_changed(current_event, caliper_event):
    """
    When the speed of the video is changed.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    caliper_event.update({
        'action': 'ChangedSpeed',
        'type': 'MediaEvent'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context'].get('course_id'),
        'ip': current_event.get('ip')
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['actor'].update({
        'name': current_event.get('username'),
        'type': 'Person'
    })
    event_info = json.loads(current_event['event'])
    caliper_event['object'] = {
        'id': current_event.get('referer'),
        'type': 'VideoObject',
        'duration': duration_isoformat(timedelta(
            seconds=event_info.pop('duration')
        )),
    }
    caliper_event['target'] = {
        'id': current_event['referer'],
        'type': 'MediaLocation',
        'currentTime': duration_isoformat(timedelta(
            seconds=event_info.pop('current_time')
        ))
    }
    caliper_event['object']['extensions'] = event_info
    return caliper_event


def play_video(current_event, caliper_event):
    """
    When a user selects the video player's play control,
    the player emits a play_video event.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """

    event_info = json.loads(current_event['event'])

    caliper_event.update({
        'action': 'Started',
        'type': 'MediaEvent',
        'target': {
            'currentTime': duration_isoformat(timedelta(
                seconds=event_info['currentTime']
            )),
            'id': current_event['referer'],
            'type': 'MediaLocation'
        }
    })

    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context'].get('course_id'),
        'ip': current_event.get('ip')
    })

    caliper_event['referrer']['type'] = 'WebPage'

    caliper_event['actor'].update({
        'name': current_event.get('username'),
        'type': 'Person'
    })

    caliper_event['object'] = {
        'id': current_event.get('referer'),
        'type': 'VideoObject',
        'duration': duration_isoformat(timedelta(
            seconds=event_info.pop('duration')
        )),
        'extensions': {
            'id': event_info.get('id'),
            'code': event_info.get('code'),
        }
    }
    return caliper_event


def load_video(current_event, caliper_event):
    """
    When the video is fully rendered and ready to play,
    the browser or mobile app emits a load_video event.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    caliper_event.update({
        'action': 'Retrieved',
        'type': 'Event'
    })

    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context'].get('course_id'),
        'ip': current_event.get('ip')
    })

    caliper_event['referrer']['type'] = 'WebPage'

    caliper_event['actor'].update({
        'name': current_event.get('username'),
        'type': 'Person'
    })

    event_info = json.loads(current_event['event'])

    caliper_event['object'] = {
        'id': current_event.get('referer'),
        'type': 'VideoObject',
        'duration': duration_isoformat(timedelta(
            seconds=event_info.pop('duration')
        )),
        'extensions': {
            'id': event_info.get('id'),
            'code': event_info.get('code'),
        }
    }

    return caliper_event


def seek_video(current_event, caliper_event):
    """
    A browser emits seek_video events when a user selects a user interface control to go to a different point in the
    video file.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    current_event_details = json.loads(current_event['event'])
    caliper_event.update({
        'action': 'JumpedTo',
        'type': 'MediaEvent',
        'object': {
            'duration': duration_isoformat(
                timedelta(seconds=current_event_details['duration'])),
            'extensions': {
                'code': current_event_details['code'],
                'id': current_event_details['id'],
                'type': current_event_details['type'],
            },
            'id': current_event['referer'],
            'type': 'VideoObject'
        },
        'target': {
            'id': current_event['referer'],
            'type': 'MediaLocation',
            'currentTime': duration_isoformat(
                timedelta(seconds=current_event_details['new_time'])),
            'extensions': {
                'old_time': duration_isoformat(
                    timedelta(seconds=current_event_details['old_time'])),
            }
        }
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['referrer']['type'] = 'WebPage'

    return caliper_event


def edx_video_closed_captions_shown(current_event, caliper_event):
    """
    When a user toggles CC to display the closed captions, the browser or mobile app emits an
    edx.video.closed_captions.shown event.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    current_event_details = json.loads(current_event['event'])
    caliper_event.update({
        'action': 'EnabledClosedCaptioning',
        'type': 'MediaEvent',
        'object': {
            'duration': duration_isoformat(
                timedelta(seconds=current_event_details['duration'])),
            'extensions': {
                'code': current_event_details['code'],
                'id': current_event_details['id']
            },
            'id': current_event['referer'],
            'type': 'VideoObject'
        },
        'target': {
            'currentTime': duration_isoformat(
                timedelta(seconds=current_event_details['current_time'])),
            'id': current_event['referer'],
            'type': 'MediaLocation'
        }
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def edx_video_closed_captions_hidden(current_event, caliper_event):
    """
    When a user toggles CC to display the closed captions, the browser or mobile app emits an
    edx.video.closed_captions.shown event.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    current_event_details = json.loads(current_event['event'])
    caliper_event.update({
        'action': 'DisabledClosedCaptioning',
        'type': 'MediaEvent',
        'object': {
            'duration': duration_isoformat(
                timedelta(seconds=current_event_details['duration'])),
            'extensions': {
                'code': current_event_details['code'],
                'id': current_event_details['id']
            },
            'id': current_event['referer'],
            'type': 'VideoObject'
        },
        'target': {
            'currentTime': duration_isoformat(
                timedelta(seconds=current_event_details['current_time'])),
            'id': current_event['referer'],
            'type': 'MediaLocation'
        }
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def hide_transcript(current_event, caliper_event):
    """
    When a user toggles Show Transcript to suppress display of the video transcript, the browser or mobile app emits a
    hide_transcript event.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    current_event_details = json.loads(current_event['event'])
    caliper_event.update({
        'action': 'DisabledClosedCaptioning',
        'type': 'MediaEvent',
        'object': {
            'duration': duration_isoformat(
                timedelta(seconds=current_event_details['duration'])),
            'extensions': {
                'code': current_event_details['code'],
                'id': current_event_details['id']
            },
            'id': current_event['referer'],
            'type': 'VideoObject'
        },
        'target': {
            'currentTime': duration_isoformat(
                timedelta(seconds=current_event_details['current_time'])),
            'id': current_event['referer'],
            'type': 'MediaLocation'
        }
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def show_transcript(current_event, caliper_event):
    """
    When a user toggles Show Transcript to display the video transcript, the browser or mobile app emits a
    show_transcript event.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    current_event_details = json.loads(current_event['event'])
    caliper_event.update({
        'action': 'EnabledClosedCaptioning',
        'type': 'MediaEvent',
        'object': {
            'duration': duration_isoformat(
                timedelta(seconds=current_event_details['duration'])),
            'extensions': {
                'code': current_event_details['code'],
                'id': current_event_details['id']
            },
            'id': current_event['referer'],
            'type': 'VideoObject'
        },
        'target': {
            'currentTime': duration_isoformat(
                timedelta(seconds=current_event_details['current_time'])),
            'id': current_event['referer'],
            'type': 'MediaLocation'
        }
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def video_hide_cc_menu(current_event, caliper_event):
    """
    When a user closes the Language Menu for a video that has transcripts in multiple languages, the browser emits a
    video_hide_cc_menu event.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    current_event_details = json.loads(current_event['event'])
    caliper_event.update({
        'action': 'Hid',
        'type': 'Event',
        'object': {
            'duration': duration_isoformat(
                timedelta(seconds=current_event_details['duration'])),
            'extensions': {
                'code': current_event_details['code'],
                'id': current_event_details['id']
            },
            'id': current_event['referer'],
            'type': 'Frame'
        }
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip'],
        'name': current_event['name']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def video_show_cc_menu(current_event, caliper_event):
    """
    When a user opens the Language Menu for a video that has transcripts in multiple languages,
    the browser emits a video_show_cc_menu event.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    current_event_details = json.loads(current_event['event'])
    caliper_event.update({
        'action': 'Showed',
        'type': 'Event',
        'object': {
            'duration': duration_isoformat(
                timedelta(seconds=current_event_details['duration'])),
            'extensions': {
                'code': current_event_details['code'],
                'id': current_event_details['id']
            },
            'id': current_event['referer'],
            'type': 'Frame'
        }
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip'],
        'name': current_event['name']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event
