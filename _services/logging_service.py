# imports
import logging
import traceback


# config
# LOGGING_LEVEL = logging.INFO
# FORMAT = '[%(asctime)s] %(levelname)-7s %(message)s'
# logging.basicConfig(level=LOGGING_LEVEL, format=FORMAT, filename='log.log')


# builds message
#   context: the context where we're calling from
#   message: the message to log
def build_message(context, message):
    context = '[' + context + ']'
    context = context.ljust(15)
    return f'{context} {message}'

# service class that contains logging logic
class Logger:

    # init
    def __init__(self):
        pass

    def get_logger(self):
        return self

    # info log
    #   context: the context where we're calling from
    #   message: the message to log
    def info(self, context, message):
        # logging.info(build_message(context, message))
        print(build_message(context, message))

    # error log
    #   context: the context where we're calling from
    #   message: the message to log
    def error(self, context, message):
        # logging.error(build_message(context, message))
        print(build_message(context, message))

    # error log
    #   context: the context where we're calling from
    #   message: the message to log
    #   e: the exception that occurred
    def error_with_exception(self, context, message, e):
        # logging.error(build_message(context, message))
        # logging.error(build_message(context, e))
        print(build_message(context, message))
        print(build_message(context, traceback.format_exc()))
