import inspect
import logging
from pathlib import Path


def customLogger(logLevel=logging.DEBUG):
    # Create a custom logger
    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)

    # Create handlers
    c_handler = logging.StreamHandler()
    file_location = Path.cwd().parent.parent
    file_location = file_location / 'AutomationLogs'

    Path(file_location).mkdir(parents=True, exist_ok=True)
    f_handler = logging.FileHandler(file_location / "AutomationLog.log", mode='w')

    logger.setLevel(logLevel)

    # Create formatters and add to the handlers
    f_format = c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                            datefmt='%m/%d/%Y %I:%M:%S %p')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handler to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
