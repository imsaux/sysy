#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import pefile
import struct


def main():
    pe = pefile.PE("AVPlay.exe")
    for imp_dll in pe.DIRECTORY_ENTRY_IMPORT:
        print(imp_dll.dll)
        for api in imp_dll.imports:
            print(api.name)

if __name__ == "__main__":
    main()