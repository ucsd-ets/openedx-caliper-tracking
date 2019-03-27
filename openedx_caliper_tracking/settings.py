"""
All settings for Caliper Tracking app.
"""

OPENEDX_CALIPER_TRACKING_PROCESSOR = 'openedx_caliper_tracking.processor.CaliperProcessor'

OPENEDX_CALIPER_TRACKING_BACKENDS = {
    'logger': {
        'ENGINE': OPENEDX_CALIPER_TRACKING_PROCESSOR,
        'OPTIONS': {
            'name': 'tracking'
        }
    }
}

CALIPER_AUTH = {
    'CALIPER_TESTS_API_URL': '',
    'CALIPER_TESTS_API_TOKEN': '',
}
