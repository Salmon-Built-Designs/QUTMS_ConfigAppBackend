import justpy as jp
import pandas as pd

class NavBar(jp.Nav):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        nav_classes = 'text-gray-300 hover:bg-blue-700 hover:text-white px-3 py-2 rounded-none text-sm font-medium'
        #nav_classes = 'bg-white text-blue-900 px-3 py-2 rounded-none text-sm font-medium'

        root = self
        c2 = jp.Nav(classes='bg-blue-900', a=root)
        c3 = jp.Div(classes='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8', a=c2)
        c4 = jp.Div(classes='flex items-center justify-between h-16', a=c3)
        c5 = jp.Div(classes='flex items-center', a=c4)
        c6 = jp.Div(classes='flex-shrink-0', a=c5)

        headerLogo = jp.Img(classes='h-8 w-8', src='https://tailwindui.com/img/logos/workflow-mark-indigo-500.svg', alt='Workflow', a=c6)

        c8 = jp.Div(classes='hidden md:block', a=c5)
        c9 = jp.Div(classes='ml-10 flex items-baseline space-x-4', a=c8)
        menuItemHome = jp.A(href='upload', classes=nav_classes, a=c9, text='Upload')
        menuItemLog = jp.A(href='log', classes=nav_classes , a=c9, text='Log')
        menuItemAnalysis = jp.A(href='analysis', classes=nav_classes , a=c9, text='Analysis')

        

        #def button_clicked(self):
            #self.info_div.text = f'Button {msg.target.num} was clicked'



class UploadForm(jp.Form):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_classes('flex flex-col border m-3 p-5')

        input_classes = 'form-input p-2 m-1'
        button_classes = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 border border-blue-500 hover:border-transparent rounded m-1'

        root = self
        in1 = jp.Input(placeholder='Description', a=root, classes=input_classes)
        in2 = jp.Input(placeholder='Driver', a=root, classes=input_classes)
        in3 = jp.Input(placeholder='Location', a=root, classes=input_classes)
        in4 = jp.Input(placeholder='Date Recorded', a=root, classes=input_classes)
        in10 = jp.Input(type='file', classes=input_classes, a=root, multiple=True)
        submit_button = jp.Input(value='Upload Log', type='submit', a=root, classes=button_classes)

# Load data showing percent of women in different majors per year
wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

async def page():
    wp = jp.WebPage()
    my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    p = jp.P(text='Hello World!', a=wp, classes=my_paragraph_design)
    
    return wp

@jp.SetRoute('/upload')
async def homePage():
    wp = jp.WebPage()
    #wp.display_url = '/upload'
    
    root = jp.Div(a=wp)

    navBar = NavBar(a=root)

    #wm.jp.ag_grid(a=c1)  # a=wp adds the grid to WebPage wp

    body = jp.Div(classes='flex flex-col items-center justify-center h-screen', a=root)
    welcomeMsg = jp.P(a=body, text=f'Hello! Please upload a file.', classes='font-bold')
    uploadForm = UploadForm(a=body)

    return wp

@jp.SetRoute('/log')
async def logPage():
    wp = jp.WebPage()
    
    root = jp.Div(a=wp)

    navBar = NavBar(a=root)

    body = jp.Div(classes='flex flex-row items-center justify-center h-screen', a=root)
    wm.jp.ag_grid(a=body)  # a=wp adds the grid to WebPage wp

    return wp

@jp.SetRoute('/analysis')
async def logPage():
    wp = jp.WebPage()
    
    root = jp.Div(a=wp)

    navBar = NavBar(a=root)

    body = jp.Div(classes='flex flex-row items-center justify-center h-screen', a=root)

    return wp


jp.justpy(homePage)

