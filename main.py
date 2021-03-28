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


@jp.SetRoute('/upload')
async def homePage():
    wp = jp.WebPage()
    #wp.display_url = '/upload'
    
    root = jp.Div(a=wp)

    navBar = NavBar(a=root)

    border = jp.Div(classes='bg-gray-300 p-6', a=root)

    body = jp.Div(classes='bg-white flex flex-col items-center justify-center h-screen', a=border)
    welcomeMsg = jp.P(a=body, text=f'Hello! Please upload a file.', classes='font-bold')
    uploadForm = UploadForm(a=body, submit=file_input)

    copyrightMsg = jp.P(a=border, text=f'QUT Motorsport 2021', classes='text-center text-gray-600 mt-6')

    return wp


@jp.SetRoute('/log')
async def logPage():
    wp = jp.WebPage()
    
    root = jp.Div(a=wp)
    navBar = NavBar(a=root)
    border = jp.Div(classes='bg-gray-300 p-6', a=root)

    body = jp.Div(classes='flex flex-row items-center justify-center h-screen bg-white', a=border)
    log = pd.read_csv('export/1/rawMsgs.csv')
    log.jp.ag_grid(a=body)  # a=wp adds the grid to WebPage wp

    return wp

@jp.SetRoute('/analysis')
async def analysisPage():
    wp = jp.WebPage()
    
    root = jp.Div(a=wp)

    navBar = NavBar(a=root)
    border = jp.Div(classes='bg-gray-300 p-6', a=root)

    tabBar = jp.Nav(classes='flex flex-col sm:flex-row', a=border)
    tab1 = jp.Button(a=tabBar, text='BMS Voltages', classes='text-gray-600 py-4 px-6 block hover:text-blue-500 focus:outline-none text-blue-900 border-b-2 font-medium border-blue-500')
    tab2 = jp.Button(a=tabBar, text='Sendyne Temps', classes='text-gray-600 py-4 px-6 block hover:text-blue-500 focus:outline-none')

    body = jp.Div(classes='flex flex-row items-center justify-center h-screen bg-white', a=border)
    
    bmsV = pd.read_csv('export/1/BMSvoltages_0.csv')
    voltages = bmsV.loc[:, bmsV.columns != 'timestamp'] 

    bms_chart = bmsV.jp.plot(0,voltages, kind='spline', a=body, title='BMS Voltage',
               subtitle='Look at this subtitle!',
                classes='m-2 p-2 w-full h-full')

    o = bms_chart.options
    o.xAxis.title.text = 'Timestamp (ms)'
    o.yAxis.title.text = 'Voltage (mV)'
    o.plotOptions.series.marker.enabled = False

    return wp


jp.justpy(homePage)

