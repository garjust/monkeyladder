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
    """
    Retrieves the value of the configuration key for the given ladder

    If the ladder specified does not have a configration for the key the default is used
    """
    if not dictionary:
        dictionary = {}
    dictionary[key] = _get_single_config(ladder, key)
    return dictionary


def get_config(ladder, key, *keys):
    config = reduce(lambda dictionary, key: _put_single_config(ladder, key, dictionary), keys, _put_single_config(ladder, key))
    return config[key] if len(config) == 1 else config
