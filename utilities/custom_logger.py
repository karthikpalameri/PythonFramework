import inspect
import logging


def customLogger(logLevel=logging.DEBUG):
    # Create a custom logger
    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler("automation.log", mode='w')

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
