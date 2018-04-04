# -*-coding:utf-8-*-
# python3.0
import re
import time
from logging.handlers import TimedRotatingFileHandler
from threading import Lock


class XTimedRotatingFileHandler(TimedRotatingFileHandler):
    lock = Lock()

    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc)
        self.extMatch = self.extMatch.pattern.replace("-", "").replace("_", "")
        self.extMatch = re.compile(self.extMatch)
        self.suffix = self.suffix.replace("-", "").replace("_", "")
        self.processRolloverAt()

    def processRolloverAt(self):
        self.rolloverAt = time.strftime(self.suffix, time.localtime(self.rolloverAt))
        self.rolloverAt = time.mktime(time.strptime(self.rolloverAt, self.suffix))

    def doRollover(self):
        XTimedRotatingFileHandler.lock.acquire()
        try:
            if self.shouldRollover(None):
                TimedRotatingFileHandler.doRollover(self)
                self.processRolloverAt()
        finally:
            XTimedRotatingFileHandler.lock.release()
