from django.apps import AppConfig
from django.conf import settings

from .settings import (
    CALIPER_TRACKING_APP_NAME,
    CALIPER_TRACKING_BACKENDS,
    CALIPER_TRACKING_PROCESSOR,
    LOGIN_EVENT_EMITTER
)


class CaliperTrackingConfig(AppConfig):
    name = CALIPER_TRACKING_APP_NAME
    verbose_name = "Caliper Tracking"

    def ready(self):
        # To override the settings after third_party_auth.
        if settings.FEATURES.get('ENABLE_THIRD_PARTY_AUTH'):
            self._apply_third_party_auth_settings()

        self._enable_caliper_backends()

    def _apply_third_party_auth_settings(self):
        """
        Apply the settings for third party auth app.
        """
        settings.SOCIAL_AUTH_PIPELINE.append(LOGIN_EVENT_EMITTER)

    def _enable_caliper_backends(self):
        """
        Apply required settings for caliperization of events.

        Add CaliperProcessor to event tracking backends' list.
        """
        if hasattr(settings, 'EVENT_TRACKING_BACKENDS'):
            settings.EVENT_TRACKING_BACKENDS['tracking_logs']['OPTIONS']['processors'] += [
                {'ENGINE': CALIPER_TRACKING_PROCESSOR}
            ]

        if hasattr(settings, 'TRACKING_BACKENDS'):
            settings.TRACKING_BACKENDS = CALIPER_TRACKING_BACKENDS
