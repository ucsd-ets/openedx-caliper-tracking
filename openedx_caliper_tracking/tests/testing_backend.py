"""
Testing Event tracking backend module.
"""

from __future__ import absolute_import

import abc


class BaseBackend(object):
    """
    Abstract Base Class for testing event tracking backends.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def send(self, event):
        """Send event to tracker."""
        pass
