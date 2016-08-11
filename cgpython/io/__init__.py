"""
for create stream logger and file logger
usage:

from cgpython import io
io.debug('debug')

"""

import os
import sys
import inspect
import logging
import logging.handlers


# create custom level between info and warning
ORDINARY = 25
logging.addLevelName(ORDINARY, 'ORDINARY')


def createTempFile():
    """
    create temp file
    @return: temp file path
    """
    import tempfile
    return tempfile.NamedTemporayFile(suffix='.log', delete=False)


def _getCallerStatus():
    try:
        frame = sys._getframe(4)
    except Exception:
        frame = sys._getframe(3)

    fileName = frame.f_code.co_filename
    callerFrameRecorder = inspect.stack()[1]
    moduleName = inspect.getmodule(callerFrameRecorder[0]).__name__
    lineNumber = frame.f_lineno
    functionName = frame.f_code.co_name
    # For class
    if 'self' in frame.f_locals.keys():
        className = frame.f_locals['self'].__class__.__name__
        if moduleName and className and functionName:
            if functionName == '?':
                logger = ".".join((moduleName, className))
            else:
                logger = ".".join(
                    (moduleName, className, functionName))
        else:
            logger = None
    else:
        className = None
        if moduleName and functionName:
            if functionName == '?':
                logger = moduleName
            else:
                logger = ".".join([moduleName, functionName])
        else:
            logger = None
    return (logger, fileName, lineNumber)


class CgLogger(logging.Logger):
    """
    Custom logger to add 'write' method.
    """

    def write(self, msg, *args, **kwargs):
        self._log(ORDINARY, msg, args, **kwargs)


class Log(object):
    """
    class for create stream logger and file logger
    """

    def __init__(self, logger=None):
        """
        @param logger: logger instance,
               example: logging.getLogger('root')
        @type logger: logger (default:None)
        @param logLevel: the logger's level
        @type logLevel: str type(default:'debug')
        """

        if not logger:
            logName = _getCallerStatus()[0]
            self.log = CgLogger(logName)
            self._createStreamLogger()

    def _getLogLevel(self):
        if os.environ.get('DEBUG'):
            logLevel = logging.DEBUG
        elif os.environ.get('INFO'):
            logLevel = logging.INFO
        elif os.environ.get('WARNING'):
            logLevel = logging.WARNING
        elif os.environ.get('ERROR'):
            logLevel = logging.ERROR
        elif os.environ.get('CRITICAL'):
            logLevel = logging.CRITICAL
        else:
            logLevel = ORDINARY
        return logLevel

    def _createStreamLogger(self):
        """
        create default stream logger
        """

        # create console handler and set level to debug
        handler = logging.StreamHandler()
        handler.setLevel(self._getLogLevel())

        # create formatter
        formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")

        # add formatter to handler
        handler.setFormatter(formatter)

        # add handler to logger
        self.handler = handler
        self.log.addHandler(handler)

    def _createFileLogger(self, logFile=None):
        """
        create file logger
        @param logFile: file logger path
        @type logFile: str (default:None)
        """

        self.log.propagate = False

        # use temp file as logger file if user not set
        if not logFile:
            logFile = createTempFile()

        print('log:{0}'.format(logFile))
        handler = logging.handlers.RotatingFileHandler(logFile,
                                                       maxBytes=2097152,
                                                       backupCount=5)
        handler.setLevel(self._getLogLevel())
        formatter = logging.Formatter('(%(asctime)s %(filename)s[line:)'
                                      '(%(lineno)d] %(levelname)s %(message)s)')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.handler = handler


def __getLogger(logger=None, logFile=None, **kwargs):
    if logger is None:
        logger = Log().log
    return logger


# Converience functions
def info(msg, **kwargs):
    __getLogger(**kwargs).info(msg)


def debug(msg, **kwargs):
    __getLogger(**kwargs).debug(msg)


def write(msg, **kwargs):
    __getLogger(**kwargs).write(msg)


def warn(msg, **kwargs):
    __getLogger(**kwargs).warn(msg)


def error(msg, **kwargs):
    __getLogger(**kwargs).error(msg)


def critical(msg, **kwargs):
    __getLogger(**kwargs).critical(msg)
