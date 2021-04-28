import justpy as jp
import pandas as pd
import os
import socket
from backend.can_parser import *
import asyncio
import time
from backend.can_parser import *
from backend.can_ids import *
import asyncio
from frontend.NavBar import NavBar
from frontend.UploadForm import UploadForm
from frontend.Tabs import Tabs
import threading

log = []
# Setup TCP Connection for CAN1
TCP_IP = '192.168.0.7'
TCP_PORT_CAN1 = 20001
TCP_PORT_CAN2 = 20005 # Double check this
BUFFER_SIZE = 4096
ID_TYPE = 1

wp = jp.WebPage(delete_flag=False)
telem_div = jp.Span(text='Loading...', classes='text-5xl m-1 p-1 bg-gray-300 font-mono', a=wp)

async def telem_counter():
    start = (time.time_ns() // 1_000_000 )
    file_open = open("Log_" + str(start) + ".txt", 'a')
    file_raw = open("rLog_" + str(start) + ".txt", 'w+b')
    file_open.write(str(start))
    # file_raw.write(start)
    disp_msgs = []

    while True:
    #   Connect to the TCP server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT_CAN1))

        # s.send(b'\x84\x10\x50\x80\x02\x01\x02\x04\x08\x00\x00\x00\x00')
        # s.send(b'\x84\x00\x00\x06\x78\x12\x34\x56\x78\x00\x00\x00\x00')
        # Receive any data that is available for us
        data = s.recv(BUFFER_SIZE)
        file_raw.write(data)
        # print(len(data))
        # print(data)
        s.close()

        current_ms = (time.time_ns() // 1_000_000 ) - start

        # Parse the data and unwrap key from metadata
        raw_msgs = []
        idx = 0

        while True:
            # print(f"len: {len(data)} idx: {idx} remaining: {len(data)-idx}")      
            ethernetPacketInformation = data[idx]
            dataLength = (ethernetPacketInformation & 0xF)
            # CAN ID
            idx= idx+1
            canId = (data[idx] << 24 | data[idx+1] << 16 | data[idx+2] << 8 | data[idx+3] << 0)
            idx = idx + 4
            parsedData = data[idx:dataLength+idx]
            raw_msgs.append(raw_can_msg(current_ms, canId, ID_TYPE, dataLength, parsedData))
            file_open.write(str(raw_can_msg(current_ms, canId, ID_TYPE, dataLength, parsedData)) + "\n")
            idx = idx + 8
            if (idx >= len(data)-1):
                break
            # Drop the messages into an array and parse them
        # for m in raw_msgs:
        #     print(m.id)
        result = parse_can_msgs(raw_msgs, False)
        output = ""

        for msg in result:
            print(str(msg))
            disp_msgs.append(msg)
            if len(disp_msgs) >= 30:
                telem_div.delete_components()
                # del disp_msgs[0]
                for i in disp_msgs:
                    elem = jp.P()
                    elem.text = str(i)
                    telem_div.add(elem)
                disp_msgs = []    
        jp.run_task(wp.update())  
        await asyncio.sleep(0.01)

# async def exit_program():
#     value = input("Choose Life or Death:\n")
#     if (value == "Death"):
#         sys.exit("You have chosen Death")

async def telem_init():
    # x = threading.Thread(target=exit_program)
    # x.start()
    jp.run_task(telem_counter())

async def telem_test():
    return wp

jp.justpy(telem_test, host='0.0.0.0', port=80, startup=telem_init)
