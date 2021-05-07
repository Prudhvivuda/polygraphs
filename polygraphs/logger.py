"""
Basic logging infrastructure for the PolyGraphs project
"""
import os
import logging
import logging.config

import yaml


_LOGGER_NAME = 'polygraphs'


def _getlogger():
    """
    Creates the PolyGraph logger.
    """
    # Load default logging configuration for polygraphs
    directory, _ = os.path.split(__file__)
    fname = os.path.join(directory, 'logging.yaml')
    assert os.path.isfile(fname)
    fstream = open(fname, 'r')
    try:
        config = yaml.load(fstream, Loader=yaml.CLoader)
    except ImportError:
        config = yaml.load(fstream, Loader=yaml.Loader)
    logging.config.dictConfig(config)

    # Reduced warning level name
    logging.addLevelName(logging.WARNING, "WARN")

    # Create logger instance
    logger = logging.getLogger(_LOGGER_NAME)
    return logger


# The PolyGraph logger
_root = _getlogger()


def getlogger():
    """
    Returns the PolyGraph logger.
    """
    return _root
