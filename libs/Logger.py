import os
import time


TIME_FORMAT = "%d/%m/%Y %H:%M:%S"


class Log:
    def __init__(self, log_name, output_type="print, file"):
        self.log_name = log_name
        self.output_type = output_type.replace(" ", "").split(",")

        if "print" in self.output_type:
            self.structurePrintLog = "{flag}[{log}][{time}] {string}"
        if "file" in self.output_type:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            self.logFile = open(f"logs/{log_name}.log", "w")
            self.structurePrintLog = "{flag}[{time}] {string}"

    def write(self, string, flag=""):
        if "print" in self.output_type:
            if flag == "E":
                print_flag = "\033[01;31mE: \033[00m"
            elif flag == "W":
                print_flag = "\033[01;33mW: \033[00m"
            elif flag:
                print_flag = f"{flag}: "
            else:
                print_flag = ""

            print(self.structurePrintLog.format(flag=print_flag, log=self.log_name, time=time.strftime(TIME_FORMAT), string=string))
        else:
            if flag:
                flag = f"{flag}: "
            self.file.write(self.structurePrintLog.format(flag=flag, time=time.strftime(TIME_FORMAT), string=string))

    def close(self):
        if "file" in self.output_type:
            self.logFile.close()
        if "print" in self.output_type:
            print("--- (LOG END) ---")
