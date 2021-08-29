import logging


# config
LOGGING_LEVEL = logging.INFO
FORMAT = '[%(asctime)s] %(levelname)-7s %(message)s'
logging.basicConfig(level=LOGGING_LEVEL, format=FORMAT, filename='log.log')


class Logger:

    # init
    def __init__(self, uptime_service):
        self.uptime_service = uptime_service

    def get_logger(self):
        return self

    # builds message
    def build_message(self, context, message):
        context = '[' + context + ']'
        context = context.ljust(15)
        return f'{self.uptime_service.get().ljust(18)} : {context} {message}'

    # info log
    def info(self, context, message):
        logging.info(self.build_message(context, message))

    # error log
    def error(self, context, message):
        logging.error(self.build_message(context, message))

    # error log
    def error_with_exception(self, context, message, e):
        logging.error(self.build_message(context, message))
        logging.error(e)
