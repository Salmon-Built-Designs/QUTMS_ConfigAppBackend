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

log = []

wp = jp.WebPage(delete_flag=False)

# Setup TCP Connection for CAN1
TCP_IP = '192.168.0.7'
TCP_PORT_CAN1 = 20001
TCP_PORT_CAN2 = 20005 # Double check this
BUFFER_SIZE = 4096
ID_TYPE = 1

async def telem_counter():
    start = (time.time_ns() // 1_000_000 )
    while True:
    #   Connect to the TCP server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT_CAN1))

        data = s.recv(BUFFER_SIZE)

        s.close()

        current_ms = (time.time_ns() // 1_000_000 ) - start

        # Parse the data and unwrap key from metadata
        raw_msgs = []
        idx = 0

        while True:
            print(f"len: {len(data)} idx: {idx} remaining: {len(data)-idx}")      
            ethernetPacketInformation = data[idx]
            dataLength = (ethernetPacketInformation & 0xF)
            # CAN ID
            idx= idx+1
            canId = (data[idx] << 24 | data[idx+1] << 16 | data[idx+2] << 8 | data[idx+3] << 0)
            idx = idx + 4
            parsedData = data[idx:dataLength+idx]
            raw_msgs.append(raw_can_msg(current_ms, canId, ID_TYPE, dataLength, parsedData))
            idx = idx + 8
            if (idx >= len(data)-1):
                break
            # Drop the messages into an array and parse them
            
        result = parse_can_msgs(raw_msgs, False)
        output = ""
        for msg in result:
            element = jp.P()
            element.text = str(msg)
            log.append(element)
        
        jp.run_task(wp.update())
        await asyncio.sleep(0.1)


async def telem_init():
    jp.run_task(telem_counter())

async def telem_test():
    root = jp.Div(a=wp, classes='h-screen flex flex-col')
    navBar = NavBar(a=root)
    border = jp.Div(classes='bg-gray-300 p-6 flex flex-col flex-1', a=root)

    if(True):

        tabBar = jp.Nav(classes='flex flex-col sm:flex-row', a=border)
        tab1 = jp.Button(a=tabBar, text='Raw Data Log', classes='text-gray-600 py-2 px-6 block hover:text-blue-500 focus:outline-none text-blue-900 border-b-2 font-medium border-blue-500')

        logbody = jp.Div(classes='flex flex-1 bg-white justify-center', a=border)

        global log
        grid = jp.AgGrid(a=logbody, classes='', style='height: full; width: 100%; margin: 0em')
        grid.load_pandas_frame(log)

    else:
        logbody = jp.Div(classes='flex flex-1 bg-white justify-center items-center', a=border)
        jp.P(text = 'Telemetry Not Transmitting', classes='text-gray-600 font-medium', a=logbody)

    copyrightMsg = jp.P(a=border, text=f'QUT Motorsport 2021', classes='bg-gray-300 text-center justify-center text-gray-600 pt-6')
    return wp

jp.justpy(telem_test, host='0.0.0.0', port=80, startup=telem_init)