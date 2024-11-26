import logging
import os
import sys
import time

from types import FrameType
from typing import cast

from loguru import logger

from core import path_conf
from core.conf import settings


class Logger:
    """
    输出日志文件至文件和控制台
    """

    def __init__(self):
        # 文件命名
        f"Fast_{time.strftime('%Y-%m-%d', time.localtime()).replace('-', '_')}.log"
        info_log_path = os.path.join(path_conf.LOG_DIR, "Fast_{time:YYYY-MM-DD}_info.log")
        error_log_path = os.path.join(path_conf.LOG_DIR, "Fast_{time:YYYY-MM-DD}_error.log")
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 判断日志文件夹是否存在，不存则创建
        if not os.path.exists(path_conf.LOG_DIR):
            os.makedirs(path_conf.LOG_DIR)

        # 日志输出格式

        # 控制台输出格式
        self.logger.add(sys.stdout,format=settings.LOGURU_STD_FORMAT,)

        # info日志写入文件
        self.logger.add(info_log_path,  # 写入目录指定文件
                        format=settings.LOGURU_FILE_FORMAT,
                        encoding='utf-8',
                        retention='7 days',  # 设置历史保留时长
                        backtrace=True,  # 回溯
                        diagnose=True,  # 诊断
                        enqueue=True,  # 异步写入
                        rotation="00:00",  # 每日更新时间
                        filter=lambda record: 'INFO' in str(record['level']).upper(),
                        # rotation="5kb",  # 切割，设置文件大小，rotation="12:00"，rotation="1 week"
                        # filter="my_module"  # 过滤模块
                        # compression="zip"   # 文件压缩
                        )

        # error日志写入文件
        self.logger.add(error_log_path,
                        format=settings.LOGURU_FILE_FORMAT,
                        encoding='utf-8',
                        retention='7 days',  # 设置历史保留时长
                        backtrace=True,  # 回溯
                        diagnose=True,  # 诊断
                        enqueue=True,  # 异步写入
                        rotation="00:00",  # 每日更新时间
                        filter=lambda record: 'ERROR' in str(record['level']).upper(),
                        )
    def init_config(self):
        LOGGER_NAMES = ("uvicorn.asgi",
                        "uvicorn.access",
                        "uvicorn",
                        "sqlalchemy",
                        "sqlalchemy.engine.Engine")

        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in LOGGER_NAMES:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.propagate=False
            logging_logger.handlers = [InterceptHandler()]

    def get_logger(self):
        return self.logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


Loggers = Logger()

log = Loggers.get_logger()