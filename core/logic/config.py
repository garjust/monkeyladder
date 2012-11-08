from core.models import LadderConfiguration, LadderConfigurationKey

import logging
logger = logging.getLogger('monkeyladder')


def _get_single_config(ladder, key):
    config_key = LadderConfigurationKey.objects.get(key=key)
    try:
        config = LadderConfiguration.objects.get(ladder=ladder, key=config_key)
        logger.debug("Found configuration for %s and ladder %s" % (key, ladder))
    except LadderConfiguration.DoesNotExist:
        config = LadderConfiguration.objects.get(ladder=None, key=config_key)
        logger.debug("Using default configuration for %s and ladder %s" % (key, ladder))
    return config.value()


def _put_single_config(ladder, key, dictionary=None):
    if not dictionary:
        dictionary = {}
    dictionary[key] = _get_single_config(ladder, key)
    return dictionary


def get_config(ladder, key, *keys):
    """
    Retrieves the configuration values for each key passed in
    """
    config = reduce(lambda dictionary, key: _put_single_config(ladder, key, dictionary), keys, _put_single_config(ladder, key))
    return config[key] if len(config) == 1 else config
