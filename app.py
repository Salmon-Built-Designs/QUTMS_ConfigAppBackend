import justpy as jp
import pandas as pd
import os
import base64
import socket
from frontend.NavBar import NavBar
from frontend.UploadForm import UploadForm
from frontend.Tabs import Tabs
from backend.can_parser import *
from backend.can_ids import *


log_cache = None

# Load data showing percent of women in different majors per year
#wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def live_telem():
    # Setup TCP Connection for CAN1
    TCP_IP = '192.168.0.7'
    TCP_PORT_CAN1 = 20001
    TCP_PORT_CAN2 = 20005 # Double check this
    BUFFER_SIZE = 4096
    ID_TYPE = 1

    while True:
	    # Connect to the TCP server
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.connect((TCP_IP, TCP_PORT_CAN1))

	    # Recieve any data that is available for us
	    data = s.recv(BUFFER_SIZE)
	    s.close()

	    # Parse the data and unwrap key from metadata
	    raw_msgs = []
	    ethernetPacketInformation = data[0]
	    dataLength = (ethernetPacketInformation & 0xF)
	    # CAN ID
	    canId = (data[1] << 24 | data[2] << 16 | data[3] << 8 | data[4] << 0)
	    parsedData = data[5:dataLength+5]

	    #Drop the messages into an array and parse them
	    raw_msgs.append(raw_can_msg(0, canId, ID_TYPE, dataLength, parsedData))
        
	    # result = parse_can_msgs(raw_msgs, False)

        new_log = log_container(parse_can_msgs(raw_msgs), metadata)
        # Isolate voltages
        new_log.bms_voltages = compile_voltages(raw_msgs)

	    print(result)
        return new_log


@jp.SetRoute('/log')
async def logPage():
    wp = jp.WebPage()
    live_telem()
    root = jp.Div(a=wp, classes='h-screen flex flex-col')
    navBar = NavBar(a=root)
    border = jp.Div(classes='bg-gray-300 p-6 flex flex-col flex-1', a=root)
    
    global log_cache

    if(log_cache != None):

        tabBar = jp.Nav(classes='flex flex-col sm:flex-row', a=border)
        tab1 = jp.Button(a=tabBar, text='Raw Data Log', classes='text-gray-600 py-2 px-6 block hover:text-blue-500 focus:outline-none text-blue-900 border-b-2 font-medium border-blue-500')

        body = jp.Div(classes='flex flex-1 bg-white justify-center', a=border)

        log = log_cache.msgs_dataframe
        grid = jp.AgGrid(a=body, classes='', style='height: full; width: 100%; margin: 0em')
        grid.load_pandas_frame(log)
        
        # Need to work out a way to auto size columns
        #grid.options.columnDefs[0].cellStyle = ['width:2000']
        #await grid.run_api('autoSizeAllColumns()', wp)
    else:
        body = jp.Div(classes='flex flex-1 bg-white justify-center items-center', a=border)
        jp.P(text = 'Please upload a file first.', classes='text-gray-600 font-medium', a=body)

    copyrightMsg = jp.P(a=border, text=f'QUT Motorsport 2021', classes='bg-gray-300 text-center justify-center text-gray-600 pt-6')

    return wp

@jp.SetRoute('/analysis')
async def analysisPage():
    wp = jp.WebPage(data={'tab': 'id2556'})

    root = jp.Div(a=wp, classes='h-screen flex flex-col')
    NavBar(a=root)
    border = jp.Div(classes='bg-gray-300 p-6 flex flex-col flex-1', a=root)

    global log_cache

    if(log_cache != None):

        t = Tabs(a=border, classes='flex flex-1 w-full', style='', animation=False, content_height=100)

        # BMS voltages
        divBMS = jp.Div(style=Tabs.wrapper_style, delete_flag=True)
        bmsV = log_cache.bms_voltages[0]
        voltages = bmsV.loc[:, bmsV.columns != 'timestamp'] 

        bms_chart = bmsV.jp.plot(0,voltages, kind='spline', a=divBMS,
                    classes='p-2 w-full h-full', use_cache=False)

        o = bms_chart.options
        o.title.text = 'BMS Voltage'
        o.xAxis.title.text = 'Timestamp (ms)'
        o.yAxis.title.text = 'Voltage (mV)'
        o.plotOptions.series.marker.enabled = False
        
        t.add_tab('idbms', 'BMS Voltage', divBMS)

        # Sendyne Temperatures
        # divTemps = jp.Div(style=Tabs.wrapper_style, delete_flag=True)
        # temps = log_cache.bms_voltages[1]
        # temperatures = temps.loc[:, temps.columns != 'timestamp'] 

        # temp_chart = temps.jp.plot(0,temperatures, kind='spline', a=divTemps,
        #             classes='p-2 w-full h-full', use_cache=False)

        # o2 = temp_chart.options
        # o2.title.text = 'Sendyne Temperatures'
        # o2.xAxis.title.text = 'Timestamp (ms)'
        # o2.yAxis.title.text = 'Temperature (C)'
        # o2.plotOptions.series.marker.enabled = False
        test = jp.Div(style=Tabs.wrapper_style, delete_flag=True)
        wipBody = jp.Div(classes='flex flex-1 bg-white justify-center items-center', a=test)
        jp.P(text = 'To be added. WIP.', classes='text-gray-600 font-medium', a=wipBody)

        
        t.add_tab('idtemp', 'BMS Temperatures', test)
        t.add_tab('idSendyne', 'Sendyne', test)
        t.add_tab('idOther', 'Other Data', test)
    else:
        body = jp.Div(classes='flex flex-1 bg-white justify-center items-center', a=border)
        jp.P(text = 'Please upload a file first.', classes='text-gray-600 font-medium', a=body)

    copyrightMsg = jp.P(a=border, text=f'QUT Motorsport 2021', classes='bg-gray-300 text-center justify-center text-gray-600 pt-6')


    return wp

my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4],
            animation: false
        }, {
            name: 'John',
            data: [5, 7, 3],
            animation: false
        }]
}
"""

@jp.SetRoute('/tabs')
async def tabsPage():
    wp = jp.WebPage(data={'tab': 'id2556'})

    root = jp.Div(a=wp, classes='h-screen flex flex-col')
    navBar = NavBar(a=root)
    border = jp.Div(classes='bg-gray-300 p-6 flex flex-col flex-1', a=root)

    t = Tabs(a=border, classes='flex flex-1 w-full', style='', animation=True, content_height=100)
    for chart_type in ['BMS Voltages', 'Temps']:
        d = jp.Div(style=Tabs.wrapper_style, delete_flag=True)
        my_chart = jp.HighCharts(a=d, classes='p-5 w-full h-full', style='', options=my_chart_def, use_cache=False)
        my_chart.options.chart.type = 'spline'
        my_chart.options.title.text = f'Chart of Type {chart_type.capitalize()}'
        my_chart.options.subtitle.text = f'Subtitle {chart_type.capitalize()}'
        t.add_tab(f'id{chart_type}', f'{chart_type}', d)






    copyrightMsg = jp.P(a=border, text=f'QUT Motorsport 2021', classes='bg-gray-300 text-center justify-center text-gray-600 pt-6')


    return wp


# jp.justpy(homePage, host='0.0.0.0', port=80)
jp.justpy(logPage, host='0.0.0.0', port=80)