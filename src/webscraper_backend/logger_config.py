import logging

def setup_logger(level=logging.DEBUG, filename="src\\webscraper_backend\\scraper.log", console_output=True):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    file_handler = logging.FileHandler(filename, mode="w")
    file_handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # handler for console output
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    # Unit Test
    logger = setup_logger()
    logger.debug('debug-message')
    logger.info('info-message')
    logger.warning('warning-message')
    logger.error('error-message')
    logger.critical('critical-message')
