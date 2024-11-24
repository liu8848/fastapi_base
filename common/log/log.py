import inspect
import logging
import os

from sys import stderr, stdout

from asgi_correlation_id import correlation_id
from loguru import logger

from core import path_conf
from core.conf import settings


class InterceptHandler(logging.Handler):
    """默认日志处理器：继承自logging.Handler"""

    def emit(self, record: logging.LogRecord):
        # 获取关联的日志等级
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.LOG_ROOT_LEVEL)

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        if 'uvicorn.access' in name or 'watchfiles.main' in name:
            logging.getLogger(name).propagate = False
        else:
            logging.getLogger(name).propagate = True

    logger.remove()

    def correlation_id_filter(record) -> bool:
        cid = correlation_id.get(settings.LOG_CID_DEFAULT_VALUE)
        record['correlation_id'] = cid[: settings.LOG_CID_UUID_LENGTH]
        return True

    logger.configure(
        handlers=[
            {
                'sink': stdout,
                'level': settings.LOG_STDOUT_LEVEL,
                'filter': lambda record: correlation_id_filter(record) and record['level'].no <= 25,
                'format': settings.LOG_STD_FORMAT,
            },
            {
                'sink': stderr,
                'level': settings.LOG_STDERR_LEVEL,
                'filter': lambda record: correlation_id_filter(record) and record['level'].no >= 30,
                'format': settings.LOG_STD_FORMAT,
            },
        ]
    )


def set_customize_logfile():
    log_path = path_conf.LOG_DIR
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    log_stdout_file = os.path.join(log_path, settings.LOG_STDOUT_FILENAME)
    log_stderr_file = os.path.join(log_path, settings.LOG_STDERR_FILENAME)

    log_config = {
        'rotation': '10MB',
        'retention': '15 days',
        'compression': 'tar.gz',
        'enqueue': True,
        'format': settings.LOG_FILE_FORMAT,
    }

    logger.add(
        str(log_stdout_file),
        level=settings.LOG_STDOUT_LEVEL,
        **log_config,
        backtrace=False,
        diagnose=False,
    )

    logger.add(
        str(log_stderr_file),
        level=settings.LOG_STDERR_LEVEL,
        **log_config,
        backtrace=False,
        diagnose=False,
    )


log = logger
