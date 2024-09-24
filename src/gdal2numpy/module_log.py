import logging

Logger = None


def init_logger():
    """
    init_logger - Initialize the logger
    """
    if Logger is None:
        print(
            "Logger initialized with format [%(levelname)-8s][%(asctime)s] %(message)s")
        logging.basicConfig(format="[%(levelname)-8s] %(message)s")
        Logger = logging.getLogger(__name__)
        Logger.setLevel(logging.CRITICAL)


def set_level(verbose, debug):
    """
    set_level - Set the log level
    """
    init_logger()
    if verbose:
        Logger.setLevel(logging.INFO)
    if debug:
        Logger.setLevel(logging.DEBUG)
