#!/usr/bin/python
#Title           : APP-Clean-Cache
#Description     : This will clear Mem Cache.
#Author          : Shekhar Raut
#Date            : 2013.12.12
#Version         : 0.1
#Usage           : APP-Clean-Cache
#Notes           :
#Python_Version  : 2.6.6
#==============================================================================
import os
sn=os.system("sync")
sc=os.system("/sbin/sysctl -w vm.drop_caches=3")
dc=os.system("/sbin/sysctl -w vm.drop_caches=0")
cc_command1 = "sn, str(&&), sc, str(&&), dc"

