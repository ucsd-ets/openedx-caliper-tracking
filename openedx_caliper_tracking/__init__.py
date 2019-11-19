"""
Apply required settings for caliperization of events.

Add CaliperProcessor to event tracking backends' list.
"""
from django.conf import settings as django_settings

from openedx_caliper_tracking import processor  # noqa: F401
from openedx_caliper_tracking.settings import OPENEDX_CALIPER_TRACKING_BACKENDS, OPENEDX_CALIPER_TRACKING_PROCESSOR

default_app_config = 'openedx_caliper_tracking.apps.CaliperTrackingConfig'

if hasattr(django_settings, 'EVENT_TRACKING_BACKENDS'):
    django_settings.EVENT_TRACKING_BACKENDS['tracking_logs']['OPTIONS']['processors'] += [
        {'ENGINE': OPENEDX_CALIPER_TRACKING_PROCESSOR}
    ]

if hasattr(django_settings, 'TRACKING_BACKENDS'):
    django_settings.TRACKING_BACKENDS = OPENEDX_CALIPER_TRACKING_BACKENDS

