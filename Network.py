# -*- coding:utf-8 -*-

import subprocess
import re
from socket import *
class network():
    @staticmethod
    def find_all_ip(platform):
        ipstr = str('([0-9]{1,3}\.){3}[0-9]{1,3}').encode()
        if platform == "Darwin" or platform == "Linux":
            ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
            output = ipconfig_process.stdout.read()
            ip_pattern = re.compile('(inet %s)' % ipstr)
            if platform == "Linux":
                ip_pattern = re.compile('(inet addr:%s)' % ipstr)
            pattern = re.compile(ipstr)
            iplist = []
            for ipaddr in re.finditer(ip_pattern, str(output)):
                ip = pattern.search(ipaddr.group())
                if ip.group() != "127.0.0.1":
                    iplist.append(ip.group())
            return iplist
        elif platform == "Windows":
            ipconfig_process = subprocess.Popen("ipconfig", stdout=subprocess.PIPE)
            output = ipconfig_process.stdout.readlines()
            ip_pattern = re.compile("IPv4 (\. )*: %s" % ipstr)
            pattern = re.compile(ipstr)
            iplist = []
            for l in output:
                if b'IPv4' in l:
                    iplist.append(l)
            return iplist

    @staticmethod
    def find_all_mask(platform):
        ipstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
        maskstr = '0x([0-9a-f]{8})'
        if platform == "Darwin" or platform == "Linux":
            ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
            output = ipconfig_process.stdout.read()
            mask_pattern = re.compile('(netmask %s)' % maskstr)
            pattern = re.compile(maskstr)
            if platform == "Linux":
                mask_pattern = re.compile(r'Mask:%s' % ipstr)
                pattern = re.compile(ipstr)
            masklist = []
            for maskaddr in mask_pattern.finditer(str(output)):
                mask = pattern.search(maskaddr.group())
                if mask.group() != '0xff000000' and mask.group() != '255.0.0.0':
                    masklist.append(mask.group())
            return masklist
        elif platform == "Windows":
            ipconfig_process = subprocess.Popen("ipconfig", stdout=subprocess.PIPE)
            output = ipconfig_process.stdout.read()
            mask_pattern = re.compile(r"Subnet Mask (\. )*: %s" % ipstr)
            pattern = re.compile(ipstr)
            masklist = []
            for maskaddr in mask_pattern.finditer(str(output)):
                mask = pattern.search(maskaddr.group())
                if mask.group() != '255.0.0.0':
                    masklist.append(mask.group())
            return masklist

    @staticmethod
    def get_broad_addr(ipstr, maskstr):
        iptokens = map(int, ipstr.split("."))
        masktokens = map(int, maskstr.split("."))
        broadlist = []
        for i in range(len(iptokens)):
            ip = iptokens[i]
            mask = masktokens[i]
            broad = ip & mask | (~mask & 255)
            broadlist.append(broad)
        return '.'.join(map(str, broadlist))

    @staticmethod
    def find_all_broad(platform):
        ipstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
        if platform == "Darwin" or platform == "Linux":
            ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
            output = (ipconfig_process.stdout.read())
            broad_pattern = re.compile('(broadcast %s)' % ipstr)
            if platform == "Linux":
                broad_pattern = re.compile(r'Bcast:%s' % ipstr)
            pattern = re.compile(ipstr)
            broadlist = []
            for broadaddr in broad_pattern.finditer(str(output)):
                broad = pattern.search(broadaddr.group())
                broadlist.append(broad.group())
            return broadlist
        elif platform == "Windows":
            iplist = network.find_all_ip(platform)
            masklist = network.find_all_mask(platform)
            broadlist = []
            for i in range(len(iplist)):
                broadlist.append(network.get_broad_addr(iplist[i], masklist[i]))
            return broadlist


    @staticmethod
    def broadcast_server():
        HOST = '<broadcast>'
        PORT = 54321

        ADDR = (HOST, PORT)

        udpCliSock = socket(AF_INET, SOCK_DGRAM)
        udpCliSock.bind(('', 0))
        udpCliSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        while True:
            data = b'haha'
            if not data:
                break
            print("sending -> %s" % data)
            udpCliSock.sendto(data, ADDR)

        udpCliSock.close()

    @staticmethod
    def broadcast_client():
        PORT = 12345
        BUFSIZE = 1024

        udpSerSock = socket(AF_INET, SOCK_DGRAM)
        udpSerSock.bind(('', PORT))
        while True:
            data, addr = udpSerSock.recvfrom(BUFSIZE)
            print('...received ->%s  %s' % (addr, data))
