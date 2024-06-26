# imports
import sys
import colorlog
import logging
from   logging.handlers import RotatingFileHandler
from   pythonjsonlogger import jsonlogger

# set logger name = module name
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Stream handler. date format is ISO-8601
streamHandler = colorlog.StreamHandler(stream=sys.stdout)  # send logs to stdout instead of stderr
fmtStream = colorlog.ColoredFormatter("%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s")  # stream format
streamHandler.setFormatter(fmtStream)
streamHandler.setLevel(logging.DEBUG)  # set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.addHandler(streamHandler)

# File handler. date format is ISO-8601
# rotate and delete log files
fileHandler = RotatingFileHandler("/Users/richardcasey/Downloads/critical_care/cc_logs/logs.txt", backupCount=5, maxBytes=5000000) # five log file rotations; rotate log filename at 5 Mb; delete oldest file
# fileHandler = RotatingFileHandler("/home/ubuntu/critical_care/cc_logs/logs.txt", backupCount=5, maxBytes=5000000) # five log file rotations; rotate log filename at 5 Mb; delete oldest file  
fmtJson = jsonlogger.JsonFormatter(
    "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
    rename_fields={"levelname": "severity", "asctime": "timestamp"},
    datefmt="%Y-%m-%dT%H:%M:%SZ",
) # json file format
fileHandler.setFormatter(fmtJson)
fileHandler.setLevel(logging.DEBUG) # set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.addHandler(fileHandler)

# Uncaught exceptions handler. 
# log these as CRITICAL.  KeyboardInterrupt is treated as normal termination of the script.
def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Error: unhandled exception", exc_info=(exc_type, exc_value, exc_traceback)) # create a critical level log message with info from the except hook.
sys.excepthook = handle_unhandled_exception # assign the excepthook to the handler

# for testing the module
if __name__ == "__main__":
    # Demonstration of logging at various levels
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")