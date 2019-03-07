"""
All settings for Caliper Tracking app.
"""

CALIPER_TRACKING_PROCESSOR = 'caliper_tracking.processor.CaliperProcessor'

CALIPER_TRACKING_BACKENDS = {
    'logger': {
        'ENGINE': CALIPER_TRACKING_PROCESSOR,
        'OPTIONS': {
            'name': 'tracking'
        }
    }
}
