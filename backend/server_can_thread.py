import os
import socket
import time
from can_parser import parse_can_msgs, raw_can_msg
from can_storage import *

import numpy as np

def thread_CAN():
    start = (time.time_ns() // 1_000_000 )

    TCP_IP_MAIN = '192.168.0.7'
    TCP_IP_INV = '192.168.0.8'
    TCP_PORT_CAN1 = 20001
    TCP_PORT_CAN2 = 20005
    BUFFER_SIZE = 65536

    #setup_storage()

    #add_bms_temp(1,0,2,[1,2])

    #print(bms_temp_data[0])

    while True:
        #time.sleep(0.01)
        try:
            print("inv1")
            sock_inv1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_inv1.connect((TCP_IP_INV, TCP_PORT_CAN1))
        except KeyboardInterrupt:
            exit()
        except:
            print("Failed to connect to CAN INV1 server")
            continue

        try:
            print("main1")
            sock_main1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_main1.connect((TCP_IP_MAIN, TCP_PORT_CAN1))
        except KeyboardInterrupt:
            exit()
        except:
            print("Failed to connect to CAN MAIN1 server")
            sock_inv1.close()
            continue

        try:
            print("main2")
            sock_main2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_main2.connect((TCP_IP_MAIN, TCP_PORT_CAN2))
        except KeyboardInterrupt:
            exit()
        except:
            print("Failed to connect to CAN MAIN2 server")
            sock_main1.close()
            sock_inv1.close()
            continue

        print("connected")

        break

    while True:
        
        print("req data")
        # Receive any main1data that is available for us
        data_inv1 = sock_inv1.recv(BUFFER_SIZE)
        data_main1 = sock_main1.recv(BUFFER_SIZE)
        data_main2 = sock_main2.recv(BUFFER_SIZE)

        print("got data")

        # sock_inv1.close()
        # sock_main1.close()
        # sock_main2.close()

        current_ms = (time.time_ns() // 1_000_000 ) - start

        timestamp_bytes = current_ms.to_bytes(4,byteorder="little")
        # with open(f"storage/{str(start)}_raw_main1.cc", 'ab+') as f_raw_main1:
        #     f_raw_main1.write(timestamp_bytes)
        #     f_raw_main1.write((len(data_main1)).to_bytes(4,byteorder="little"))
        #     f_raw_main1.write(data_main1)

        # with open(f"storage/{str(start)}_raw_main2.cc", 'ab+') as f_raw_main2:
        #     f_raw_main2.write(timestamp_bytes)
        #     f_raw_main2.write((len(data_main2)).to_bytes(4,byteorder="little"))
        #     f_raw_main2.write(data_main2)

        # with open(f"storage/{str(start)}_raw_inv1.cc", 'ab+') as f_raw_inv1:
        #     f_raw_inv1.write(timestamp_bytes)
        #     f_raw_inv1.write((len(data_inv1)).to_bytes(4,byteorder="little"))
        #     f_raw_inv1.write(data_inv1)

        with open(f"storage/{str(start)}_raw_all.cc", 'ab+') as f_raw_all:
            f_raw_all.write(timestamp_bytes)
            f_raw_all.write((len(data_main1) + len(data_main2) + len(data_inv1)).to_bytes(4,byteorder="little"))
            f_raw_all.write(data_main1)
            f_raw_all.write(data_main2)
            f_raw_all.write(data_inv1)

        data_combined = [data_inv1, data_main2, data_main1]
        # print(data_combined)

        # Parse the main1data and unwrap key from metadata
        channel_ID = ["CAN1", "CAN4", "CAN2"]
        raw_msgs_all = [[],[],[]]
        idx = 0

        for i in range(len(data_combined)):
            idx = 0
            raw_data = data_combined[i]
            while True:
                if (idx+13 >= len(raw_data)):
                    break
                # print(f"len: {len(raw_data)} idx: {idx} remaining: {len(raw_data)-idx}")
                ethernetPacketInformation = raw_data[idx]
                dataLength = (ethernetPacketInformation & 0xF)
                ID_TYPE = (ethernetPacketInformation >> 7) & 0b1
                # CAN ID
                idx= idx+1
                canId = (raw_data[idx] << 24 | raw_data[idx+1] << 16 | raw_data[idx+2] << 8 | raw_data[idx+3] << 0)
                idx = idx + 4
                parsedData = raw_data[idx:dataLength+idx]

                raw_msg = raw_can_msg(current_ms, canId, ID_TYPE, dataLength, parsedData)
                #print(raw_msg)

                raw_msgs_all[i].append(raw_msg)

                idx = idx + 8

        parsed_msgs_all = []
        for raw_msgs in raw_msgs_all:
            parsed = parse_can_msgs(raw_msgs, False)
            for msg in parsed:
                if msg != None:
                    print(msg)
            parsed_msgs_all.append(parsed)