from django.conf import settings as django_settings

from . import processor
from .settings import CALIPER_TRACKING_BACKENDS, CALIPER_TRACKING_PROCESSOR


default_app_config = 'caliper_tracking.apps.CaliperTrackingConfig'


def _enable_caliper_backends():
        """
        Apply required settings for caliperization of events.

        Add CaliperProcessor to event tracking backends' list.
        """
        if hasattr(django_settings, 'EVENT_TRACKING_BACKENDS'):
            django_settings.EVENT_TRACKING_BACKENDS['tracking_logs']['OPTIONS']['processors'] += [
                {'ENGINE': CALIPER_TRACKING_PROCESSOR}
            ]

        if hasattr(django_settings, 'TRACKING_BACKENDS'):
            django_settings.TRACKING_BACKENDS = CALIPER_TRACKING_BACKENDS


_enable_caliper_backends()
