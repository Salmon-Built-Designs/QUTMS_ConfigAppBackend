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
    BUFFER_SIZE = 4096

    #setup_storage()

    #add_bms_temp(1,0,2,[1,2])

    #print(bms_temp_data[0])

    while True:
        time.sleep(0.05)
        try:
            sock_inv1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_inv1.connect((TCP_IP_INV, TCP_PORT_CAN1))

            sock_main1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_main1.connect((TCP_IP_MAIN, TCP_PORT_CAN1))

            sock_main2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_main2.connect((TCP_IP_MAIN, TCP_PORT_CAN2))
        except KeyboardInterrupt:
            exit()
        except:
            print("Failed to connect to CAN server")
            continue

        # Receive any main1data that is available for us
        data_inv1 = sock_inv1.recv(BUFFER_SIZE)
        data_main1 = sock_main1.recv(BUFFER_SIZE)
        data_main2 = sock_main2.recv(BUFFER_SIZE)

        sock_main1.close()
        sock_main2.close()
        sock_inv1.close()

        current_ms = (time.time_ns() // 1_000_000 ) - start

        timestamp = (f"{str(current_ms)}\n").encode('ascii')

        with open(f"storage/{str(start)}_raw_main1.cc", 'ab') as f_raw_main1:
            f_raw_main1.write(timestamp)
            f_raw_main1.write(data_main1)
            f_raw_main1.write(b'\n')
        with open(f"storage/{str(start)}_raw_main2.cc", 'ab') as f_raw_main2:
            f_raw_main2.write(timestamp)
            f_raw_main2.write(data_main2)
            f_raw_main2.write(b'\n')
        with open(f"storage/{str(start)}_raw_inv1.cc", 'ab') as f_raw_inv1:
            f_raw_inv1.write(timestamp)
            f_raw_inv1.write(data_inv1)
            f_raw_inv1.write(b'\n')
            
        with open(f"storage/{str(start)}_raw_all.cc", 'ab') as f_raw_all:
            f_raw_all.write(timestamp)
            f_raw_all.write(data_main1)
            f_raw_all.write(data_main2)
            f_raw_all.write(data_inv1)
            f_raw_all.write(b'\n')

        data_combined = [data_inv1, data_main1, data_main2]

        # Parse the main1data and unwrap key from metadata
        channel_ID = ["CAN1", "CAN4", "CAN2"]
        raw_msgs_all = [[],[],[]]
        idx = 0
        for i in range(len(data_combined)):
            raw_data = data_combined[i]
            while True:
                # print(f"len: {len(raw_data)} idx: {idx} remaining: {len(raw_data)-idx}")      
                ethernetPacketInformation = raw_data[idx]
                dataLength = (ethernetPacketInformation & 0xF)
                # CAN ID
                idx= idx+1
                canId = (raw_data[idx] << 24 | raw_data[idx+1] << 16 | raw_data[idx+2] << 8 | raw_data[idx+3] << 0)
                idx = idx + 4
                parsedData = raw_data[idx:dataLength+idx]

                raw_msgs_all[i].append(raw_can_msg(current_ms, canId, ID_TYPE, dataLength, parsedData))

                #parsedmain1.write(str(raw_can_msg(current_ms, canId, ID_TYPE, dataLength, parsedData)) + "\n")

                idx = idx + 8
                if (idx >= len(raw_data)-1):
                    break

        parsed_msgs_all = []
        for raw_msgs in raw_msgs_all:
            parsed_msgs_all.append(parse_can_msgs(raw_msgs, False))