# -*- coding: utf-8 -*-
# @Time    : 2021/4/6 9:53
# @Author  : Merlin.Xie

import logging
import os
import time

import colorlog


class Log:

    @classmethod
    def init(cls, log_name=None, directory=None, level='INFO', debug=True):
        """
        :param log_name:日志保存位置，默认使用Y_M_D/H_M_S.log方式
        :param directory:日志保存目录，默认使用./Y_M_D
        :param level:日志级别
        :param debug:是否在控制台输出
        """
        timeDay = str(time.strftime("%Y_%m_%d", time.localtime()))
        timeSecond = str(time.strftime("%H_%M_%S", time.localtime()))
        try:
            if not directory:
                directory = timeDay
                os.mkdir(r"{}".format(timeDay))
            else:
                os.mkdir(r"{}".format(directory))
        except FileExistsError:
            pass

        if not log_name:
            cls.log_name = timeSecond
        else:
            cls.log_name = log_name
        cls.log_path = r'{}/{}.log'.format(directory, cls.log_name)
        cls.level = level
        cls.debug = debug
        cls.log_colors_config = {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        return cls.__logger()


    @classmethod
    def __logger(cls):
        # 创建logger
        cls.logger = logging.getLogger(cls.log_name)
        cls.logger.setLevel(level=logging.DEBUG)

        # 日志级别
        level = eval("logging." + cls.level)
        # 日志格式
        fmt = logging.Formatter('%(asctime)s    %(filename)s    --->  [%(levelname)s]   '
                                '%(funcName)s   line:%(lineno)d  : %(message)s')

        # 设置handler
        cls.File_handler = logging.FileHandler(cls.log_path)
        cls.File_handler.setLevel(level=level)
        cls.File_handler.setFormatter(fmt=fmt)
        cls.logger.addHandler(cls.File_handler)

        if cls.debug:
            cls.Console_hander = logging.StreamHandler()
            cls.Console_hander.setLevel(level)
            fmt = colorlog.ColoredFormatter(fmt='%(log_color)s %(asctime)s    %(filename)s    --->  '
                                                '[%(levelname)s]   %(funcName)s   line:%(lineno)d  : %(message)s',
                                            log_colors=cls.log_colors_config)
            cls.Console_hander.setFormatter(fmt)
            cls.logger.addHandler(cls.Console_hander)
        print("手动执行初始化logger")
        print(cls.logger)
        return cls.logger

    @classmethod
    def shutdown(cls):
        cls.logger.removeHandler(cls.File_handler)
        cls.logger.removeHandler(cls.Console_hander)
        logging.shutdown()


if __name__ == '__main__':
    """
    最好把类单独拿出来并且赋值给某个变量，这样在后面可以单独使用shutdown方法清除缓存
    log = Log; logger = log.init()

    当然也可以不用赋值直接 logger = Log.init
    """
    log = Log

    # logger一定需要手动初始化
    logger = log.init()

    logger.info('info message')
    logger.debug('debug message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')

