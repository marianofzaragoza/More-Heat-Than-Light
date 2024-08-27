import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

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
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())

    self.addHandler(ch)

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

    log.debug('hello debug')
    log.info('hello info')
    log.warning('hello warning')
    log.error('hello error')
    log.critical('hello critical')

