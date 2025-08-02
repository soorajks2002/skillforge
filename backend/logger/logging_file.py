import logging


logger = logging.getLogger('app.logger')

# root logger level
logger.setLevel(logging.DEBUG)

# Console handler (CLI)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


# File handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s -- %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


for i in range(10):
    logger.debug(f"Debug message {i}")
    logger.info(f"Info message {i}")
    logger.warning(f"Warning message {i}")
    logger.error(f"Error message {i}")
    logger.critical(f"Critical message {i}")
