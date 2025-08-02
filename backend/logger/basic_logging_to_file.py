import logging


logging.basicConfig(
    # min level to print
    level=logging.DEBUG,
    # save to file, instead of printing to console
    filename="basic_logging.log",
    # mode to write
    filemode="w",
    )


logging.debug("This is a debug message")
logging.info("This is an info message")

# Default level is warning, hence the above two will not be printed
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")