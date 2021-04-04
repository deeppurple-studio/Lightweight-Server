import subprocess

server = subprocess.Popen(["python3", "serverInit.py"])
server.wait()
