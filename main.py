import justpy as jp
import pandas as pd

button_classes = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 border border-blue-500 hover:border-transparent rounded m-2'
input_classes = 'border m-2 p-2'

# Load data showing percent of women in different majors per year
wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

async def page():
    wp = jp.WebPage()
    my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    p = jp.P(text='Hello World!', a=wp, classes=my_paragraph_design)
    
    return wp

async def homePage():
    wp = jp.WebPage()
    wp.display_url = '/upload'
    root = jp.Div(a=wp)

    c1 = jp.Div(classes='' ,a=root)
    c2 = jp.Nav(classes='bg-blue-900', a=c1)
    c3 = jp.Div(classes='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8', a=c2)
    c4 = jp.Div(classes='flex items-center justify-between h-16', a=c3)
    c5 = jp.Div(classes='flex items-center', a=c4)
    c6 = jp.Div(classes='flex-shrink-0', a=c5)
    headerLogo = jp.Img(classes='h-8 w-8', src='https://tailwindui.com/img/logos/workflow-mark-indigo-500.svg', alt='Workflow', a=c6)
    c8 = jp.Div(classes='hidden md:block', a=c5)
    c9 = jp.Div(classes='ml-10 flex items-baseline space-x-4', a=c8)
    menuItemHome = jp.A(href='upload', classes='bg-white text-blue-900 px-3 py-2 rounded-none text-sm font-medium', a=c9, text='Upload')
    menuItemLog = jp.A(href='log', classes='text-gray-300 hover:bg-blue-700 hover:text-white px-3 py-2 rounded-none text-sm font-medium', a=c9, text='Log')
    

    #wm.jp.ag_grid(a=c1)  # a=wp adds the grid to WebPage wp

    body = jp.Div(classes='flex items-center justify-center h-screen', a=c1)
    uploadForm = jp.Form(a=body, classes='flex flex-col border m-3 p-5 w-max')

    in1 = jp.Input(placeholder='Description', a=uploadForm, classes='form-input p-2')
    in2 = jp.Input(placeholder='Driver', a=uploadForm, classes='form-input p-2')
    in3 = jp.Input(placeholder='Location', a=uploadForm, classes='form-input p-2')
    in4 = jp.Input(placeholder='Date Recorded', a=uploadForm, classes='form-input p-2')
    in10 = jp.Input(type='file', classes='form-input', a=uploadForm, multiple=True)
    submit_button = jp.Input(value='Submit Form', type='submit', a=uploadForm, classes=button_classes)
    #in1.file_div = jp.Div(a=uploadForm)

    return wp



jp.justpy(homePage)

