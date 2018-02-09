# -*- coding:utf-8 -*-

import datetime


class sy_date():
    @staticmethod
    def datetime_format(date=None, mode=1):
        """
        获取特定格式的日期时间字符串
        """
        if date is None:
            date = datetime.datetime.now()
        if mode == 1:
            return str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日'
        elif mode == 2:
            return date.strftime('%Y%m%d%H%M%S')
        elif mode == 3:
            return date.strftime('%m/%d/%Y')
        elif mode == 4:
            return str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日 ' + str(date.hour).zfill(
                2) + ':' + str(date.minute).zfill(2) + ':' + str(date.second).zfill(2)
        elif mode == 5:
            return date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return date


import logging
import inspect
import os

class sy_log():
    def get_logger(self, _name):

        logger = logging.getLogger(_name)

        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        if not os.path.exists(os.path.join(dirpath, 'log')):
            os.makedirs(os.path.join(dirpath, 'log'))
        handler = logging.FileHandler(os.path.join(dirpath, 'log', sy_date._datetime_format(mode=2) + ".log"))

        formatter = logging.Formatter('%(asctime)s %(name)-12s [line:%(lineno)d] %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger


import re

class sy_check():
    def check_ip(self, _str):
        return re.match(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", _str)


import subprocess
import re
from socket import *


class netutil():
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
            iplist = netutil.find_all_ip(platform)
            masklist = netutil.find_all_mask(platform)
            broadlist = []
            for i in range(len(iplist)):
                broadlist.append(netutil.get_broad_addr(iplist[i], masklist[i]))
            return broadlist


    @staticmethod
    def broadcast_server():
        HOST = '<broadcast>'
        PORT = 21567

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
        HOST = '127.0.0.1'
        PORT = 12345
        BUFSIZE = 1024

        udpSerSock = socket(AF_INET, SOCK_DGRAM)
        udpSerSock.bind(('', PORT))
        while True:
            data, addr = udpSerSock.recvfrom(BUFSIZE)
            print('...received ->%s  %s' % (addr, data))

if __name__ == '__main__':
    pass