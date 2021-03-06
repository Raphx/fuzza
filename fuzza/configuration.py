"""
fuzza.configuration
-------------------

This module is used to handle operations related to reading, storing,
and writing of fuzzer configuration.
"""
import logging

from pathlib import Path

from ruamel.yaml import YAML

from .logger import get_logger

LOG = get_logger(__name__)
IS_DEBUG = LOG.isEnabledFor(logging.DEBUG)

# The filename of configuration file
FILENAME = 'fuzza.cfg'


def _get_cfile_path(directory, extension):
    """
    Returns the path to configuration file.

    Args:
        directory (str): Directory containing the configuration file.
        extension (str): The filename extension of the configuration
            file.

    Returns:
        Path to the configuration file.
    """
    return (
        Path(directory) /
        (FILENAME + '.' + extension)
    )


def load(config):
    """
    Load and normalize a raw configuration. Empty values in the raw
    configuration are omitted.

    Args:
        config (dict): The fuzzer raw configuration.

    Returns:
        dict: The normalized configuration.
    """
    conf = {}

    for key, value in config.items():
        if value is not None and value != '':
            conf[key] = value

    return conf


def to_file(config, dest_dir='', extension='yml'):
    """
    Store configuration to file.

    Args:
        config (dict): The configuration to be stored.
        dest_dir (str): Directory to store the configuration file.
            Defaults to empty string, which is the current
            src_dir of script execution.
        extension (str): The extension determining the configuration
            file format. Defaults to 'yml'.
    """
    cfile = _get_cfile_path(dest_dir, extension)

    if extension == 'yml':
        yaml = YAML(pure=True)
        yaml.dump(config, cfile)

    LOG.info('Stored configuration to file: %s', cfile)

    if IS_DEBUG:
        LOG.debug('Config: %s', config)


def from_file(src_dir='', extension='yml'):
    """
    Read configuration from file.

    Args:
        src_dir (str): Directory containing the configuration file.
            Defaults to empty string, which is the current
            directory of script execution.
        extension (str): The extension determining the configuration
            file format. Defaults to 'yml'.

    Returns:
        The configuration read from file.
    """
    cfile = _get_cfile_path(src_dir, extension)

    conf = {}
    if extension == 'yml':
        yaml = YAML(typ='safe', pure=True)
        conf = yaml.load(cfile)

    LOG.info('Read configuration from file: %s', cfile)

    if IS_DEBUG:
        LOG.debug('Config: %s', conf)

    return conf
