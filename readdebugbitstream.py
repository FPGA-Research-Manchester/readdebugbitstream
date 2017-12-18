#!/usr/bin/env python3
import sys
import csv
from binascii import hexlify

#def getDevice(DeviceID):
#    Devices = {
#        0x03722093: "XC7Z010",
#        0x03727093: "XC7Z020",
#        0x0484A093: "XCZU9EG",
#    }
#    return Devices.get(DeviceID, "")

def main(argv):
    filename = argv[0]
    fileCSV = ('devices.csv')
    print filename
    f = open(filename, 'r+')
    f_csv = open(fileCSV, 'r+')

    reader = csv.reader(f_csv)

    Sync = 0

    B1 = 0
    B2 = 0
    B3 = 0
    B4 = 0

    addr = 0
    pre_addr = 0
    row_addr = 0
    pre_row_addr = 0
    BA = 0      # Block type [25:23]
    TB = 0      # Top/bottom bit [22]
    RA = 0      # Row address [21:17]
    MJA= 0      # Column address [16:7]
    MNA= 0      # Minor address [6:0]
    row_BA = 0      # Block type [25:23]
    row_TB = 0      # Top/bottom bit [22]
    row_RA = 0      # Row address [21:17]
    NoOfFr = 0
    NoOfFrPerRow = 0

    pre_BA = BA
    pre_TB = TB
    pre_RA = RA
    pre_MJA= MJA
    pre_row_BA = row_BA
    pre_row_TB = row_TB
    pre_row_RA = row_RA

    Device= ""
    DevFa = ""
    while True:
#    for i in range(200):
        B4 = B3
        B3 = B2
        B2 = B1

        byte = f.read(1)

        if byte == '':
            break

        byte = hexlify(byte)
        B1 = int(byte, 16)
#        print B4,B3,B2,B1
#        print hex(B4),hex(B3),hex(B2),hex(B1)
        if B4 == 0xaa and B3 == 0x99 and B2 == 0x55 and B1 == 0x66:
            print "Sync Word!"
            Sync = 1
            break

    if Sync == 1:
        while True:
            word = f.read(4)

            if word == '':
                break

            word = int(hexlify(word), 16)

            if word == 0x30018001:
                word1 = f.read(4)
                word1 = hexlify(word1)
#                print word1
                for row in reader:
                    if int(word1, 16) == int(row[0], 16):
                        Device =  row[1]
#                word1 = int(hexlify(word1), 16)
#                Device= getDevice(word1)
                if Device == "":
                    print "Device is not supported!"
                    break
                else:
                    print "Found a device:",Device
                    DevFa = Device[2:4]
                    print "Device family:",DevFa

            if word == 0x30002001:
#                print "FAR register commands"
                word = f.read(4)
                word1 = f.read(4)
                word2 = f.read(4)
                word3 = f.read(4)

                word = int(hexlify(word), 16)
                word3 = int(hexlify(word3), 16)

                if DevFa == "7Z":
                    BA = (word & 0x03800000) >> 23
                    TB = (word & 0x00400000) >> 22
                    RA = (word & 0x003E0000) >> 17
                    row_BA = (word & 0x03800000) >> 23
                    row_TB = (word & 0x00400000) >> 22
                    row_RA = (word & 0x003E0000) >> 17
                    MJA= (word & 0x0001FF80) >> 7
                    MNA= (word & 0x0000007F)
                    addr = (word & ~(0x0000007F))
                    row_addr = (word & ~(0x0001FFFF))
                elif DevFa == "ZU" or DevFa == "VU":
                    BA = (word & 0x07000000) >> 24
                    RA = (word & 0x00FC0000) >> 18
                    row_BA = (word & 0x07000000) >> 24
                    row_RA = (word & 0x00FC0000) >> 18
                    MJA= (word & 0x0003FF00) >> 8
                    MNA= (word & 0x000000FF)
                    addr = (word & ~(0x000000FF))
                    row_addr = (word & ~(0x0003FFFF))
                else:
                    BA = (word & 0x03800000) >> 23
                    TB = (word & 0x00400000) >> 22
                    RA = (word & 0x003E0000) >> 17
                    row_BA = (word & 0x03800000) >> 23
                    row_TB = (word & 0x00400000) >> 22
                    row_RA = (word & 0x003E0000) >> 17
                    MJA= (word & 0x0001FF80) >> 7
                    MNA= (word & 0x0000007F)
                    addr = (word & ~(0x0000007F))
                    row_addr = (word & ~(0x0001FFFF))

                # check if that frame contains no configuration data
                if pre_addr == addr:
                    NoOfFr = NoOfFr + 1
                else:
                    if DevFa == "7Z":
                        print "address:",hex(pre_addr),"column BA:",pre_BA,"TB:",pre_TB,"RA:",pre_RA,"MJA:",pre_MJA,"has no. of frames:",NoOfFr
                        NoOfFr = 1
                        pre_BA = BA
                        pre_TB = TB
                        pre_RA = RA
                        pre_MJA= MJA
                        pre_addr = addr
                    elif DevFa == "ZU":
                        print "address:",hex(pre_addr),"column BA:",pre_BA,"RA:",pre_RA,"MJA:",pre_MJA,"has no. of frames:",NoOfFr
                        NoOfFr = 1
                        pre_BA = BA
                        pre_RA = RA
                        pre_MJA= MJA
                        pre_addr = addr
                    else:
                        print "address:",hex(pre_addr),"column BA:",pre_BA,"TB:",pre_TB,"RA:",pre_RA,"MJA:",pre_MJA,"has no. of frames:",NoOfFr
                        NoOfFr = 1
                        pre_BA = BA
                        pre_TB = TB
                        pre_RA = RA
                        pre_MJA= MJA
                        pre_addr = addr

                # check if that frame contains no configuration data
                if pre_row_addr == row_addr:
                    NoOfFrPerRow = NoOfFrPerRow + 1
                else:
                    if DevFa == "7Z":
                        print "Row BA:",pre_row_BA,"TB:",pre_row_TB,"RA:",pre_row_RA,"has no. of frames:",NoOfFrPerRow
                        NoOfFrPerRow = 1
                        pre_row_BA = row_BA
                        pre_row_TB = row_TB
                        pre_row_RA = row_RA
                        pre_row_addr = row_addr
                    elif DevFa == "ZU":
                        print "Row BA:",pre_row_BA,"RA:",pre_row_RA,"has no. of frames:",NoOfFrPerRow
                        NoOfFrPerRow = 1
                        pre_row_BA = row_BA
                        pre_row_RA = row_RA
                        pre_row_addr = row_addr
                    else:
                        print "Row BA:",pre_row_BA,"TB:",pre_row_TB,"RA:",pre_row_RA,"has no. of frames:",NoOfFrPerRow
                        NoOfFrPerRow = 1
                        pre_row_BA = row_BA
                        pre_row_TB = row_TB
                        pre_row_RA = row_RA
                        pre_row_addr = row_addr

            if word == 0x30010001 and DevFa == "6V":
                word = f.read(4)
                word1 = f.read(4)

                word = int(hexlify(word), 16)
                word1 = int(hexlify(word1), 16)

                BA = (word & 0x00E00000) >> 21
                TB = (word & 0x00100000) >> 20
                RA = (word & 0x000F8000) >> 15
                row_BA = (word & 0x00E00000) >> 21
                row_TB = (word & 0x00100000) >> 20
                row_RA = (word & 0x000F8000) >> 15
                MJA= (word & 0x00007F80) >> 7
                MNA= (word & 0x0000007F)
                addr = (word & ~(0x0000007F))
                row_addr = (word & ~(0x00007FFF))

                # check if that frame contains no configuration data
                if pre_addr == addr:
                    NoOfFr = NoOfFr + 1
                else:
                    print "address:",hex(pre_addr),"column BA:",pre_BA,"TB:",pre_TB,"RA:",pre_RA,"MJA:",pre_MJA,"has no. of frames:",NoOfFr
                    NoOfFr = 1
                    pre_BA = BA
                    pre_TB = TB
                    pre_RA = RA
                    pre_MJA= MJA
                    pre_addr = addr

                # check if that frame contains no configuration data
                if pre_row_addr == row_addr:
                    NoOfFrPerRow = NoOfFrPerRow + 1
                else:
                    print "Row BA:",pre_row_BA,"TB:",pre_row_TB,"RA:",pre_row_RA,"has no. of frames:",NoOfFrPerRow
                    NoOfFrPerRow = 1
                    pre_row_BA = row_BA
                    pre_row_TB = row_TB
                    pre_row_RA = row_RA
                    pre_row_addr = row_addr

            if word == 0x30010001 and DevFa == "7V":
                word = f.read(4)
                word1 = f.read(4)

                word = int(hexlify(word), 16)
                word1 = int(hexlify(word1), 16)

                BA = (word & 0x03800000) >> 23
                TB = (word & 0x00400000) >> 22
                RA = (word & 0x003E0000) >> 17
                row_BA = (word & 0x03800000) >> 23
                row_TB = (word & 0x00400000) >> 22
                row_RA = (word & 0x003E0000) >> 17
                MJA= (word & 0x0001FF80) >> 7
                MNA= (word & 0x0000007F)
                addr = (word & ~(0x0000007F))
                row_addr = (word & ~(0x0001FFFF))

                # check if that frame contains no configuration data
                if pre_addr == addr:
                    NoOfFr = NoOfFr + 1
                else:
                    print "address:",hex(pre_addr),"column BA:",pre_BA,"TB:",pre_TB,"RA:",pre_RA,"MJA:",pre_MJA,"has no. of frames:",NoOfFr
                    NoOfFr = 1
                    pre_BA = BA
                    pre_TB = TB
                    pre_RA = RA
                    pre_MJA= MJA
                    pre_addr = addr

                # check if that frame contains no configuration data
                if pre_row_addr == row_addr:
                    NoOfFrPerRow = NoOfFrPerRow + 1
                else:
                    print "Row BA:",pre_row_BA,"TB:",pre_row_TB,"RA:",pre_row_RA,"has no. of frames:",NoOfFrPerRow
                    NoOfFrPerRow = 1
                    pre_row_BA = row_BA
                    pre_row_TB = row_TB
                    pre_row_RA = row_RA
                    pre_row_addr = row_addr
    else:
        print "Couldn't find the SYNC word - Invalid bitfile"

    print "end of file!"
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
