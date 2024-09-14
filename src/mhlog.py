import logging
#https://betterstack.com/community/guides/logging/python/python-logging-best-practices/
# https://github.com/keeprocking/pygelf
class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    #format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s [%(threadName)s] (%(filename)s:%(lineno)d) "

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
class Logger(logging.Logger):
  def __init__(self, name, level=logging.NOTSET):
    super().__init__(name, level)
    ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)

    ch.setFormatter(CustomFormatter())

    self.addHandler(ch)

    # log to file
    file_handler = logging.FileHandler(filename='debug/mh.log')
    file_handler.setFormatter(CustomFormatter())
    file_handler.setLevel(logging.INFO)
    self.addHandler(file_handler)

    self.extra_info = None

  def info(self, msg, *args, xtra=None, **kwargs):
    extra_info = xtra if xtra is not None else self.extra_info
    super().info(msg, *args, extra=extra_info, **kwargs)

'''
####
class MhBaseLog(logging.getLoggerClass()):
    def __init__(self, name):
        super(MhBaseLog, self).__init__(name)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        ch.setFormatter(CustomFormatter())

        self.addHandler(ch)
        
'''
#########
import logging, sys, traceback

#########3
def getLog(name, srcobject):
    """ Like logging.getLogger"""
    #if ident is not None:
    #    name = "%s.0x%x" % (name, ident)
    name = srcobject.__class__.__name__
    #name = srcobject.__module__  + srcobject.__class__.__name__

    return logging.getLogger(name)

if __name__ == "__main__":
    logging.setLoggerClass(Logger)
    log = getLog("thermomether", "this would be self")

    assert isinstance(log, Logger)
    log.setLevel(logging.DEBUG)
    
    def default_excepthook(exctype, value, tb):
        if issubclass(exctype, KeyboardInterrupt):
            sys.__excepthook__(exctype, value, tb)
            return
        #log.exception("Uncaught exception: {0}".format(str(value)))
        log.exception(''.join(traceback.format_exception(exctype, value, tb)), exc_info=(exctype, value, tb))
        log.critical("Uncaught exception", exc_info=(exctype, value, tb))
        log.exception(''.join(traceback.format_exception(exctype, value, tb)))




    # Install exception handler
    sys.excepthook = default_excepthook
    log.debug('hello debug')
    log.info('hello info')
    log.warning('hello warning')
    log.error('hello error')
    log.critical('hello critical')
    raise RuntimeError("Test unhandled")

