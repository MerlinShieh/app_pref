import subprocess as sub
import pandas as pd
from com.log import Log
class AppLogcat:
    def __init__(self, devices=None, pid=None):
        sub.call(['adb', 'start-server'], shell=True)
        self.pid = pid
        self.devices = devices

    def checkDev(self) -> bool:
        cmd_devices = 'adb devices'
        output = sub.run(cmd_devices, stdout=sub.PIPE, timeout=3, shell=True,
                         universal_newlines=True).stdout
        output_list = str(output).split('\n')
        del output_list[-2:], output_list[0]
        # print(output_list)
        for i in range(len(output_list)):
            output_list[i] = output_list[i].split('\t')
        # print(output_list)
        for i in output_list:
            return str(87872933) in i








    def __logcat(self, clear=True):
        cmd_init = 'adb shell logcat -c'
        if self.pid:
            cmd_start = 'adb shell logcat'

AppLogcat().checkDev()