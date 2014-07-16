#!/usr/local/bin/python3
# Title           : Jboss Application Start/Stop Script
# Description     : This will START/STOP/RESTART Jboss Server for TRANS
# Author          : Shekhar Raut
# Date            : 2014.06.01
# Version         : 1.1
# Usage           : python script
# Notes           : If you wish this script should run on another server, then make sure, 
#                   you have changed the variables as mentioned below.
# Python_Version  : 3.3.5  
# Software	  : Jboss-EAP-6.0
# Prerequesits	  : Set environment for Jboss
#==============================================================================
''' DEFINING VARIABLES 
-----------------------------------------------------------------------------------------------'''

japp="Jboss-App-"
ol="nohup.log"
ip="10.10.10.101"
scr="standalone.sh"
nh="nohup"
basedir="/opt/jboss-eap-6.0/standalone"
bdv="-Djboss.server.base.dir"
logdir="/opt/Logs/nohup/jboss"


import os
import time
import shutil

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    OKCYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.OKCYAN = ''
        self.BOLD  = ''
        self.UNDERLINE = ''
        self.FAIL = ''
        self.ENDC = ''

def banner():
    return print(bcolors.OKGREEN + "\t\t\t 1\a Start TRANS App"+bcolors.ENDC, "\n",  bcolors.FAIL+"\t\t\t 2\a Stop TRANS App"+bcolors.ENDC, "\n", \
bcolors.OKBLUE+"\t\t\t 3\a Restart TRANS App"+bcolors.ENDC, "\n", bcolors.HEADER + \
bcolors.OKGREEN + "\t\t\t 4\a APP Status"+bcolors.ENDC, "\n",  bcolors.HEADER + "\t\t\t 5\a Exit" + bcolors.ENDC)

def jstrbanner():
    return print(bcolors.BOLD + bcolors.OKGREEN + "\t\t Starting Application"+bcolors.ENDC)

def jstpbanner():
    return print(bcolors.BOLD + bcolors.FAIL + "\t\t Stopping Application"+bcolors.ENDC)

target = logdir + os.sep + nh + japp + time.strftime('%Y-%m-%d-%H_%M_%S') + ".log"

def status():
    PrStOp=os.popen("ps -ef | grep java").read()
    return print(PrStOp)

def pause():
    return input(bcolors.OKCYAN + "Press Enter to continue..."+bcolors.ENDC)

def logrt():
    return os.system("mv {2}/{0} {1} >/dev/null 2>&1".format(ol, target, logdir))
    
def jstart():
    return os.system("{4} {2} {5}={6} -b {1} > {3}/{0} 2>&1 &".format(ol, ip, scr, logdir, nh, bdv, basedir))

def jstop():
    return os.system("jboss-cli.sh --connect --controller={0} --command=:shutdown  >  /dev/null 2>&1 &".format(ip))

def rm_tmp():
    try:
        return shutil.rmtree(os.path.join(basedir, 'tmp'))
    except (FileNotFoundError):
        print(bcolors.FAIL+"TMP already Deleted \n"+bcolors.ENDC)
	
def pschk():
    tmp = os.popen("ps -Af").read()
    if ip not in tmp[:]:
        logrt()
        jstart()
        jstrbanner()
        pause()
    else:
        print(bcolors.BOLD+bcolors.FAIL+"Application is already running. STOP it First.... \n"+bcolors.ENDC)

running = True
while running :
    os.system("clear")
    banner()
    try:
        a = int(input(bcolors.WARNING+"Please enter your choice: \n"+bcolors.ENDC))
        if a == 1:
            pschk()
        elif a == 2:
            logrt()
            jstop()
            jstpbanner()
            time.sleep(5)
            rm_tmp()
            pause()
#            running = False
        elif a == 3:
            logrt()
            jstop()
            jstpbanner()
            time.sleep(5)
            rm_tmp()
            pschk()
#            running = False
        if a == 4:
            status()
            pause()
        elif a == 5:
            running = False
    except (ValueError,KeyboardInterrupt):
        print(bcolors.FAIL+"Please select appropriate Choice: \n"+bcolors.ENDC)
        pause()


