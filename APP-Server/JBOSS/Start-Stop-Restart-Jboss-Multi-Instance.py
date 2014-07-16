#!/usr/local/bin/python3
# Title           : Jboss Application Start/Stop Script
# Description     : This will start as well as stop Jboss Server for two instances MARS and TRANS
# Author          : Shekhar Raut
# Date            : 2014.06.01
# Version         : 1.5
# Usage           : python script
# Notes           : If you wish this script should run on another server, then make sure, 
#                   you have changed the variables as mentioned below.
# Python_Version  : 3.3.5  
# Softwares	  : Jboss-EAP-6.0
# Prerequesites	  : we are considering 2 projects of jboss 1. /opt/jboss-eap-6.0/standalone 2. /opt/jboss-eap-6.0/standalone2
#		    and you need to also create nohup directories for the same.
#		    (You can search how to run jboss for multiple instances or projects)
#               *   Set environment for Jboss
#==============================================================================
''' DEFINING VARIABLES 
-----------------------------------------------------------------------------------------------'''

japp1="JBOSS-APP-1"
japp2="JBOSS-APP-2"
ol="nohup.log"
ip1="10.10.10.101"
ip2="10.10.10.102"
scr="standalone.sh"
nh="nohup"
basedir1="/opt/jboss-eap-6.0/standalone"
basedir2="/opt/jboss-eap-6.0/standalone2"
bdv="-Djboss.server.base.dir"
logdir1="/opt/Logs/nohup/jboss-app1"
logdir2="/opt/Logs/nohup/jboss-app2"


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
    return print(bcolors.OKGREEN + "\t\t\t 1\a Start MARS App"+bcolors.ENDC, "\n",  bcolors.FAIL+"\t\t\t 2\a Stop MARS App"+bcolors.ENDC, "\n", \
bcolors.OKBLUE+"\t\t\t 3\a Restart MARS App"+bcolors.ENDC, "\n", bcolors.HEADER + \
bcolors.OKGREEN + "\t\t\t 4\a Start TRANS App"+bcolors.ENDC, "\n",  bcolors.FAIL+"\t\t\t 5\a Stop TRANS App"+bcolors.ENDC, "\n", \
bcolors.OKBLUE+"\t\t\t 6\a Restart TRANS App"+bcolors.ENDC, "\n", bcolors.OKGREEN + "\t\t\t 7\a APP Status"+bcolors.ENDC, "\n",  bcolors.OKCYAN + "\t\t\t 8\a Forcefully Stop Application (Kill Process) \n" + bcolors.ENDC, bcolors.HEADER + "\t\t\t 9\a Exit" + bcolors.ENDC)

def jstrbanner():
    return print(bcolors.BOLD + bcolors.OKGREEN + "\t\t Starting Application"+bcolors.ENDC)

def jstpbanner():
    return print(bcolors.BOLD + bcolors.FAIL + "\t\t Stopping Application"+bcolors.ENDC)

target1 = logdir1 + os.sep + nh + japp1 + time.strftime('%Y-%m-%d-%H_%M_%S') + ".log"
target2 = logdir2 + os.sep + nh + japp2 + time.strftime('%Y-%m-%d-%H_%M_%S') + ".log"

def status():
    PrStOp=os.popen("ps -ef | grep java").read()
    return print(PrStOp)

def pause():
    return input(bcolors.OKCYAN + "Press Enter to continue..."+bcolors.ENDC)

def pkill():
    k=input(bcolors.WARNING+"Please Enter Process ID: "+bcolors.ENDC)
    return os.system("kill -9 "+str(k))

def logrt1():
    return os.system("mv {2}/{0} {1} >/dev/null 2>&1".format(ol, target1, logdir1))
    
def logrt2():
    return os.system("mv {2}/{0} {1} >/dev/null 2>&1".format(ol, target2, logdir2))
    
def jstart1():
    return os.system("{4} {2} {5}={6} -b {1} > {3}/{0} 2>&1 &".format(ol, ip1, scr, logdir1, nh, bdv, basedir1))
    
def jstart2():
    return os.system("{4} {2} {5}={6} -b {1} > {3}/{0} 2>&1 &".format(ol, ip2, scr, logdir2, nh, bdv, basedir2))

def jstop1():
    return os.system("jboss-cli.sh --connect --controller={0} --command=:shutdown  >  /dev/null 2>&1 &".format(ip1))
	
def jstop2():
    return os.system("jboss-cli.sh --connect --controller={0} --command=:shutdown  >  /dev/null 2>&1 &".format(ip2))

def rm_tmp1():
    try:
        return shutil.rmtree(os.path.join(basedir1, 'tmp'))
    except (FileNotFoundError):
        print(bcolors.FAIL+"TMP already Deleted \n"+bcolors.ENDC)

def rm_tmp2():
    try:
        return shutil.rmtree(os.path.join(basedir2, 'tmp'))
    except (FileNotFoundError):
        print(bcolors.FAIL+"TMP already Deleted \n"+bcolors.ENDC)
        
def pschk1():
    tmp = os.popen("ps -Af").read()
    if ip1 not in tmp[:]:
        logrt1()
        jstart1()
        jstrbanner()
        pause()
    else:
        print(bcolors.BOLD+bcolors.FAIL+"Application is already running. STOP it First.... \n"+bcolors.ENDC)
        pause()

def pschk2():
    tmp = os.popen("ps -Af").read()
    if ip2 not in tmp[:]:
        logrt2()
        jstart2()
        jstrbanner()
        pause()
    else:
        print(bcolors.BOLD+bcolors.FAIL+"Application is already running. STOP it First.... \n"+bcolors.ENDC)
        pause()

running = True
while running :
    os.system("clear")
    banner()
    try:
        a = int(input(bcolors.WARNING+"Please enter your choice: \n"+bcolors.ENDC))
        if a == 1:
            pschk1()
        elif a == 2:
            logrt1()
            jstop1()
            jstpbanner()
            time.sleep(5)
            rm_tmp1()
            pause()

        elif a == 3:
            logrt1()
            jstop1()
            jstpbanner()
            time.sleep(9)
            rm_tmp1()
            pschk1()
        elif a == 4:
            pschk2()
        elif a == 5:
            logrt2()
            jstop2()
            jstpbanner()
            time.sleep(5)
            rm_tmp2()
            pause()
        elif a == 6:
            logrt2()
            jstop2()
            jstpbanner()
            time.sleep(9)
            rm_tmp2()
            pschk2()
        elif a == 7:
            status()
            pause()
        elif a == 8:
            status()
            pkill()
            time.sleep(2)
            status()
            pause()
        elif a == 9:
            running = False
    except (ValueError,KeyboardInterrupt):
        print(bcolors.FAIL+"Please select appropriate Choice: \n"+bcolors.ENDC)
        pause()

