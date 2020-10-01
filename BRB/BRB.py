#!/usr/bin/env python3
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import sys

def logo(logoFile):
    with open(logoFile) as dasFile:
        for line in dasFile:
            print(line, end='')


def updateTools():
    os.system("searchsploit -u")

def attackTarget():
    os.system("msfconsole msf exploit\(handler\) > load msgrpc Pass=pa55w0rd")


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
            if element.lower() == "u":
                updateTools()
                if not scansComplete:
                    runScans(sys.argv[1])
                    scansComplete = True
            elif element.lower() == "a":
                if not scansComplete:
                    runScans(sys.argv[1])
                    scansComplete = True
                attackTarget()
    else:
        print("Please supply target IP followed by parameter(s) u = update tools | a = attack target")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
