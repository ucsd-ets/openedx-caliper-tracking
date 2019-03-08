"""
All settings for Caliper Tracking app.
"""

EDX_CALIPER_TRACKING_PROCESSOR = 'edx_caliper_tracking.processor.CaliperProcessor'

EDX_CALIPER_TRACKING_BACKENDS = {
    'logger': {
        'ENGINE': EDX_CALIPER_TRACKING_PROCESSOR,
        'OPTIONS': {
            'name': 'tracking'
        }
    }
}
