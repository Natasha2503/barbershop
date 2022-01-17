import logging

class LogInfo:
    logging.basicConfig(filename="logs/loginfo.log", level=logging.INFO)
    log = logging.getLogger("inf")
