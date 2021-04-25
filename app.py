import justpy as jp
import pandas as pd
import os
import base64
from frontend.NavBar import NavBar
from frontend.UploadForm import UploadForm
from frontend.Tabs import Tabs
from backend.can_parser import *


log_cache = None

# Load data showing percent of women in different majors per year
#wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def file_input(self, msg):

    # Find the element in the form data that contains the file information
    for c in msg.form_data:
        if c.type == 'file':
            break

    for f in c.files:
        newFile = f
        print('Uploaded file found.')
        print(f'{f.name} | {f.size} | {f.type} | {f.lastModified}')

    SAVE_VOLUME = 'cache'

    if not os.path.isdir(SAVE_VOLUME):
        os.mkdir(SAVE_VOLUME)

    if not os.path.isdir(fr'{SAVE_VOLUME}/{msg.session_id}'):
        os.mkdir(fr'{SAVE_VOLUME}/{msg.session_id}')

    # Save uploaded file to cache
    savedFile = open(fr'{SAVE_VOLUME}/{msg.session_id}/log.CC', "wb")
    savedFile.write(base64.b64decode(newFile.file_content))
    savedFile.close()

    # Metadata list, need to get user info from form (to be implemented)
    metadata = [msg.session_id, 'some description', 'some date', 'some driver', 'some location']

    # Process file
    global log_cache
    log_cache = process_file(fr'{SAVE_VOLUME}/{msg.session_id}/log.CC',metadata)
    msg.page.redirect = '/log'

@jp.SetRoute('/upload')
async def homePage():
    wp = jp.WebPage()
    #wp.display_url = '/upload'
    
    root = jp.Div(a=wp, classes='h-screen flex flex-col')
    navBar = NavBar(a=root)
    border = jp.Div(classes='bg-gray-300 p-6 flex flex-col flex-1', a=root)

    body = jp.Div(classes='bg-white grid grid-rows-2 grid-flow-col gap-8 flex flex-1 items-center justify-center h-full w-full', a=border)
    welcomeCol = jp.Div(a=body, classes='row-span-2 m-3 p-5')
    formCol = jp.Div(a=body, classes='row-span-2 border m-3 p-5')
    
    welcomeMsg = jp.H1(a=welcomeCol, text=f'Hello! Welcome to ConfigApp v0.1', classes='font-bold text-lg text-right')
    uploadMsg = jp.P(a=welcomeCol, text='Upload a binary .CC file to begin.', classes='text-right')
    uploadForm = UploadForm(a=formCol, submit=file_input)

    copyrightMsg = jp.P(a=border, text=f'QUT Motorsport 2021', classes='bg-gray-300 text-center justify-center text-gray-600 pt-6')

    return wp


@jp.SetRoute('/log')
async def logPage():
    wp = jp.WebPage()
    
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


jp.justpy(homePage,host='0.0.0.0', port=80)