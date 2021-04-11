import subprocess as sub
import pandas as pd
from com import log
import os
import time
import traceback
import random

logger = log.logger


class APP:
    def __init__(self, appname='com.tencent.mm'):
        """
        :param appname: 指的需要测试的app的包名，默认为微信的包名 com.tencent.mm
        """
        self.appname = appname
        self.map = {
            'java': 'Java Heap:',
            'native': 'Native Heap:',
            'code': 'Code:',
            'stack': 'Stack:',
            'graphics': 'Graphics:',
            'private': 'Private Other:',
            'system': 'System:',
            'total': 'TOTAL:'
        }
        self.pidList = self.__getPid()
        # self.logger = logger
        pass

    def __getPid(self) -> list:
        """
        :return:  返回一个由app的pid组成的pid列表
        """
        cmd = 'adb shell ps -A | findstr {}'.format(self.appname)
        output, err = sub.Popen(
            cmd, stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, shell=True
        ).communicate()
        output = output.decode('utf-8')

        pidList = []
        for line in output.split('\n'):
            if len(line.split()):
                pidList.append(line.split()[1])
        return pidList

    def __meminfo(self, pid: int) -> dict:
        """
        :param pid: 进程的pid
        :return: eg:
        {'java': '10904', 'native': '27948', 'code': '8132', 'stack': '80', 'graphics': '12084', 'private': '6064',
         'system': '13305', 'total': '78517'}
        """
        memDict = {}
        cmd = 'adb shell dumpsys meminfo {}'.format(pid)
        output = sub.Popen(
            cmd, stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, shell=True
        )

        time.sleep(1)
        try:
            # 处理异常，可以不用关注这些
            if output.poll() != 0:
                for i in range(3):
                    if output.poll() == 0:
                        data, err = output.communicate()
                        data = data.decode('utf-8').replace('\t', ' ').replace('\r', ' ').split('\n')
                        break
                    elif output.poll() is None:
                        logger.debug('process poll is None , process is Running! loop count {}'.format(i + 1))
                        time.sleep(1)
                    else:
                        logger.error('Error! process poll Error, pid: {}'.format(output.poll()))
                        os.kill(output.poll(), 1)
                        data = []
                        break
            else:
                data, err = output.communicate()
                data = data.decode('utf-8').replace('\t', ' ').replace('\r', ' ').split('\n')
        except:
            logger.error(traceback.format_exc())
            traceback.print_exc(file=open('./file/Error.log', 'a'))
            exit(code=-1)
        for line in data:
            if self.map['java'] in line:
                memDict['java'] = line.split()[2]
            elif self.map['native'] in line:
                memDict['native'] = line.split()[2]
            elif self.map['code'] in line:
                memDict['code'] = line.split()[1]
            elif self.map['stack'] in line:
                memDict['stack'] = line.split()[1]
            elif self.map['graphics'] in line:
                memDict['graphics'] = line.split()[1]
            elif self.map['private'] in line:
                memDict['private'] = line.split()[2]
            elif self.map['system'] in line:
                memDict['system'] = line.split()[1]
            elif self.map['total'] in line:
                memDict['total'] = line.split()[1]
        return memDict

    def meminfo(self, _pid: int):
        return self.__meminfo(_pid)


if __name__ == '__main__':
    TempList = []
    app = APP()
    # pid是appname所运行的进程中随机的一个，可以自己写死
    pid = app.pidList[random.randint(0, (len(app.pidList)) - 1)]
    logger.info('APP pid is {}'.format(pid))


    def run():
        memDict = app.meminfo(pid)
        TempList.append(memDict)
        print(memDict)
        return TempList


    # LoopNumber 值用来循环的次数
    LoopNumber = 10
    logger.debug(f'Loop number is f{LoopNumber}')
    [run() for i in range(LoopNumber)]
    logger.info('Done')
    # 如果没有装pandas，可以把下面的都注释掉，这样就不会写进excel文件
    df = pd.DataFrame(data=TempList, index=list(range(LoopNumber)))
    print('\n===============================================================================\n')
    print(df)
    df.to_excel('./file/test.xlsx', sheet_name='{}'.format(pid), encoding='utf-8')
    log.shutdown()
