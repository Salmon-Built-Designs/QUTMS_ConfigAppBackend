import justpy as jp
import pandas as pd
import os
import base64
from frontend.NavBar import NavBar
from frontend.UploadForm import UploadForm
from backend.can_parser import *


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

    if not os.path.exists("cache"):
        os.mkdir("cache")

    # Save uploaded file to cache
    savedFile = open("cache/log.CC", "wb")
    savedFile.write(base64.b64decode(newFile.file_content))
    savedFile.close()

    # Process file
    process_file("cache/log.cc","")
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

    tabBar = jp.Nav(classes='flex flex-col sm:flex-row', a=border)
    tab1 = jp.Button(a=tabBar, text='Raw Data Log', classes='text-gray-600 py-2 px-6 block hover:text-blue-500 focus:outline-none text-blue-900 border-b-2 font-medium border-blue-500')

    body = jp.Div(classes='flex flex-1 bg-white justify-center', a=border)
    
    log = pd.read_csv('export/1/rawMsgs.csv')
    grid = jp.AgGrid(a=body, classes='', style='height: full; width: 100%; margin: 0em')
    grid.load_pandas_frame(log)

    #grid.options.columnDefs[0].cellStyle = ['width:2000']
    #await grid.run_api('autoSizeAllColumns()', wp)

    copyrightMsg = jp.P(a=border, text=f'QUT Motorsport 2021', classes='bg-gray-300 text-center justify-center text-gray-600 pt-6')

    return wp

@jp.SetRoute('/analysis')
async def analysisPage():
    wp = jp.WebPage()
    
    root = jp.Div(a=wp, classes='h-screen flex flex-col')
    navBar = NavBar(a=root)
    border = jp.Div(classes='bg-gray-300 p-6 flex flex-col flex-1', a=root)

    tabBar = jp.Nav(classes='flex flex-col sm:flex-row', a=border)
    tab1 = jp.Button(a=tabBar, text='BMS Voltages', classes='text-gray-600 py-2 px-6 block hover:text-blue-500 focus:outline-none text-blue-900 border-b-2 font-medium border-blue-500')
    tab2 = jp.Button(a=tabBar, text='Sendyne Temps', classes='text-gray-600 py-2 px-6 block hover:text-blue-500 focus:outline-none')

    body = jp.Div(classes='flex flex-1 bg-white', a=border)
    
    bmsV = pd.read_csv('export/1/BMSvoltages_0.csv')
    voltages = bmsV.loc[:, bmsV.columns != 'timestamp'] 

    bms_chart = bmsV.jp.plot(0,voltages, kind='spline', a=body, title='BMS Voltage',
               subtitle='Look at this subtitle!',
                classes='p-2 w-full h-full')

    o = bms_chart.options
    o.xAxis.title.text = 'Timestamp (ms)'
    o.yAxis.title.text = 'Voltage (mV)'
    o.plotOptions.series.marker.enabled = False

    copyrightMsg = jp.P(a=border, text=f'QUT Motorsport 2021', classes='bg-gray-300 text-center justify-center text-gray-600 pt-6')


    return wp


jp.justpy(homePage)

