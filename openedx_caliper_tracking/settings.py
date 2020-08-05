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

# Used for certification
CERTIFICATION_AUTH = {
    'API_URL': '',
    'API_TOKEN': '',
}
