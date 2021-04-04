import os
import time


class Log:
    def __init__(self, log_name, line_structure="{flag}[{log_name}][{time}] {log_message}", time_structure="%d-%m-%Y %H:%M:%S", output_type="console, file"):
        self.log_name = log_name
        self.line_structure = line_structure
        self.time_structure = time_structure
        self.output_type = output_type.replace(" ", "").split(",")

        if "console" in self.output_type:
            print("--- LOG [{self.log_name}] START ---")

        if "file" in self.output_type:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            self.logFile = open(f"logs/{log_name}.log", "a")

    def write(self, message, flag=""):
        if "console" in self.output_type:
            if flag == "E":
                print_flag = "\033[01;31mE: \033[00m"
            elif flag == "W":
                print_flag = "\033[01;33mW: \033[00m"
            elif flag:
                print_flag = f"{flag}: "
            else:
                print_flag = ""

            print(self.line_structure.format(flag=print_flag, log_name=self.log_name, time=time.strftime(self.time_structure), log_message=message))

        if "file" in self.output_type:
            if flag:
                flag = f"{flag}: "
            self.logFile.write(self.line_sructure.format(flag=flag, log_name=self.log_name, time=time.strftime(self.time_structure), log_message=message)+"\n")

    def close(self):
        if "file" in self.output_type:
            self.logFile.close()
        if "console" in self.output_type:
            print(f"--- (LOG {self.log_name} END) ---")
