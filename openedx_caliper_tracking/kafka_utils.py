import logging

from django.conf import settings

LOGGER = logging.getLogger(__name__)


def get_kafka_producer_configurations():
    """
    Return the configurations required to initialize the KafkaProducer object.
    """
    try:
        configurations = {}
        configurations.update(settings.CALIPER_KAFKA_SETTINGS.get('PRODUCER_CONFIG', {}))
        configurations.update(settings.CALIPER_KAFKA_AUTH_SETTINGS.get('PRODUCER_CONFIG', {}))
        return configurations

    except AttributeError as ex:
        LOGGER.exception('Invalid or no configurations are provided for KafkaProducer: %s', str(ex))
        raise
