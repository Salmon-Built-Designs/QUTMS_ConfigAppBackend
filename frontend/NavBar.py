import justpy as jp

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
        c6 = jp.Div(classes='flex-shrink', a=c5)

        headerLogo = jp.Img(classes='w-16 h-8', src='/static/frontend/images/qutms_logo.svg', alt='Workflow', a=c6)

        c8 = jp.Div(classes='', a=c5)
        c9 = jp.Div(classes='ml-5 flex items-baseline space-x-2', a=c8)
        menuItemHome = jp.A(href='upload', classes=nav_classes, a=c9, text='Upload')
        menuItemLog = jp.A(href='log', classes=nav_classes , a=c9, text='Log')
        menuItemAnalysis = jp.A(href='analysis', classes=nav_classes , a=c9, text='Analysis')

        

        #def button_clicked(self):
            #self.info_div.text = f'Button {msg.target.num} was clicked'