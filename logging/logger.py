import logging

class Logger:
    def __init__(self, name="my_project"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Formatter for the console output
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(ch)

        # You can add file handler as well if needed
        # fh = logging.FileHandler('project.log')
        # fh.setLevel(logging.DEBUG)
        # fh.setFormatter(formatter)
        # self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger
