# -*- coding: utf-8 -*-
import logging
import time
import os
import colorlog


class Log:
    def __init__(self, log_name=None, directory=None, level='INFO', debug=True):
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
            self.log_name = timeSecond
        self.log_path = r'{}/{}.log'.format(directory, self.log_name)
        self.level = level
        self.debug = debug
        self.log_colors_config = {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        self.logger = self.__logger()

    def __logger(self):
        # 创建logger
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(level=logging.DEBUG)

        # 日志级别
        level = eval("logging." + self.level)
        # 日志格式
        fmt = logging.Formatter('%(asctime)s    %(filename)s    --->  [%(levelname)s]   '
                                '%(funcName)s   line:%(lineno)d  : %(message)s')

        # 设置handler
        File_handler = logging.FileHandler(self.log_path)
        File_handler.setLevel(level=level)
        File_handler.setFormatter(fmt=fmt)
        self.logger.addHandler(File_handler)

        if self.debug:
            self.Console_hander = logging.StreamHandler()
            self.Console_hander.setLevel(level)
            fmt = colorlog.ColoredFormatter(fmt='%(log_color)s %(asctime)s    %(filename)s    --->  '
                                                '[%(levelname)s]   %(funcName)s   line:%(lineno)d  : %(message)s',
                                            log_colors=self.log_colors_config)
            self.Console_hander.setFormatter(fmt)
            self.logger.addHandler(self.Console_hander)

        return self.logger


if __name__ == '__main__':
    logger = Log(level='DEBUG').logger
    logger.debug('debug message ')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
    logger.debug(logger.name)
