import logging

#logging.basicConfig(format="[%(asctime)s][%(levelname)-8s] %(message)s")
logging.basicConfig(format="[%(levelname)-8s][%(asctime)s] %(message)s")
Logger = logging.getLogger(__name__)
Logger.setLevel(logging.INFO)
print("Logger initialized from gal2numpy")

def set_log_level(verbose, debug):
    if verbose:
        Logger.setLevel(logging.INFO)
    if debug:
        Logger.setLevel(logging.DEBUG)