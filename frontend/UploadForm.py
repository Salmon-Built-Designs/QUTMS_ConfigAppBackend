import justpy as jp

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
        in10 = jp.Input(type='file', classes=input_classes, a=root, multiple=False)
        submit_button = jp.Input(value='Upload Log', type='submit', a=root, classes=button_classes)

    