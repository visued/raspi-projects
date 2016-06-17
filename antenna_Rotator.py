import paramiko
import RPi.GPIO as GPIO
import socket
from time import sleep

__author__ =      ["Victor Sued"]
__email__ =       "visued@gmail.com"
__copyright__ =   "Copyright 2016, Victor Sued Inc."
__license__ =     "Python Sofware Foundation"
__version__ = "0.1"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)

def main():
    while verifyConnection() == False:
        forward(0.5)

def forward(x):
    GPIO.output(13, GPIO.HIGH)
    sleep(x)
    GPIO.output(13, GPIO.LOW)

def verifyConnection():
    ip="192.168.11.2"
    user="admin"
    password=''
    tout=0.5
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip, username=user, password=password, timeout=tout, compress = True,look_for_keys=False, allow_agent=False)
    except (socket.error,paramiko.AuthenticationException,paramiko.SSHException) as message:
        print "ERROR: SSH connection to "+ip+" failed: " +str(message)
        sys.exit(1)
    stdin, stdout, ssh_stderr = ssh.exec_command("interface wireless monitor wlan1 once")
    out = stdout.read().split()
    status = out[1]
    stdin.flush()
    ssh.close()

    if status == 'connected-to-ess':
        return True
    else:
        return False

main()
GPIO.cleanup()
