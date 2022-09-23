import PySimpleGUI as sg
import os,io
from PIL import Image,ImageFilter
import cv2

sg.theme("lightgreen")

imagefiletype = (("png", "*.png"), ("jpeg", "*.jpeg"), ("jpg", "*.jpg"),  ("All Files", "*.*"))

#set element window
Main_Colum = [
    [
    sg.Input(size=(25,1),key='File',visible=False), #False , True
    sg.FileBrowse(key='browse',file_types=(imagefiletype)),
    sg.Input(size=(25,1),key='file_path',visible=False),
    sg.Button('Select'),
    ],
]

Image_Colum = [
    [sg.Frame('ShowImage',[[sg.Image(size=(650,450),expand_y=True,expand_x=True,key='SImage',filename=(''))]])],
]

Menu_Colum = [
    [
    sg.Checkbox('MirrorImage',key='_mirror',default=False),
    sg.Checkbox('BlurImage',key='_blur',default=False),
    sg.Checkbox('GrayScale',key='_gray',default=False),
    ]
]

Special_Colum = [
    [sg.Checkbox('Emboss',key='_emboss',default=False),
    ]
]

Low_Coulum = [
    [sg.SaveAs(),sg.Button('Clear')],
]

Rotate_Color_Coulum = [
    [sg.Text('Rotate :')],
    [sg.Slider(range=(0,360),default_value=0,key='rotateimage_key',orientation ='')], #horizontal
]

layout = [
    [sg.Column(Main_Colum),
     sg.VSeperator(),
     sg.Text('Function : '),
     sg.Column(Menu_Colum,element_justification='right'),
     sg.VSeperator(),
     sg.Text('Special Function : '),
     sg.Column(Special_Colum)],
    [sg.vtop(sg.Column(Rotate_Color_Coulum)),sg.VSeparator(),sg.Column(Image_Colum,element_justification='left')],
]

#function to process
def process_image(a):
    image = Image.open(a)
    image.thumbnail((600,600))
    bio = io.BytesIO()
    image.save(bio,format="png")
    window['SImage'].update(data=bio.getvalue())

def gray_image():
    image = cv2.imread(values['File'])
    BAW = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    saveim = 'tranfer_image.png'
    cv2.imwrite(saveim,BAW)
    
def blur_image():
    image = cv2.imread(values['File'])
    image = cv2.blur(image,(15,15))
    saveim = 'tranfer_image.png'
    cv2.imwrite(saveim,image)
    
def BlurAGray_image():
    image = cv2.imread(values['File'])
    BAW = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    BAWim = BAW
    image = cv2.blur(BAWim,(15,15))
    saveim = 'tranfer_image.png'
    cv2.imwrite(saveim,image)

def Emboss():
    image = Image.open(values['File'])
    embossedimage = image.filter(ImageFilter.EMBOSS)
    embossedimage.thumbnail((600,600))
    embossedimage.save('tranfer_image.png')
    
def BlurEmboss():
    image = cv2.imread('tranfer_image.png')
    image = cv2.blur(image,(15,15))
    cv2.imwrite('tranfer_image.png',image)

def FlipEmboss(x):
    image = Image.open(values['File'])
    flipimage = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    embossedimage = flipimage.filter(ImageFilter.EMBOSS)
    embossedimage.thumbnail((600,600))
    embossedimage.save('tranfer_image.png')
    if x == 'normal':
        embossedimage.save('tranfer_image.png')
    if x == 'blur':
        blurflip = cv2.imread('tranfer_image.png')
        blurflipimage = cv2.blur(blurflip,(15,15))
        cv2.imwrite('tranfer_image.png',blurflipimage)

def flip_image(x):
    saveim = 'tranfer_image.png'
    if x == 1:
        image = Image.open(values['File'])
        flipimage = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        flipimage.thumbnail((600,600))
        flipimage.save('tranfer_image.png')
    if x == 2:
        image = cv2.imread(values['File'])
        image = cv2.blur(image,(15,15))
        flipimage = cv2.flip(image, 1)
        cv2.imwrite(saveim,flipimage)
    if x == 3:
        image = cv2.imread(values['File'])
        BAW = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        flipimage = cv2.flip(BAW, 1)
        cv2.imwrite(saveim,flipimage)
    if x == 4:
        image = cv2.imread(values['File'])
        image = cv2.blur(image,(15,15))
        BAW = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        flipimage = cv2.flip(BAW, 1)
        cv2.imwrite(saveim,flipimage)


def rotate(x):
    image = Image.open('tranfer_image.png')
    rotateimage = image.rotate(x)
    rotateimage.thumbnail((600,600))
    rotateimage.save('tranfer_image.png')

def hentai():
    layout = [
        [sg.Input('',key='hentai_input'),sg.Button('ok')]
    ]
    return sg.Window('',layout,finalize=True)

#create window
window = sg.Window('GUI หน้าโง่', layout, size=(870,500))

#while loop
while True:
    event, values = window.read()
    print("event:", event, "values: ",values)
    rotate_values_image = values['rotateimage_key']
    if event == sg.WIN_CLOSED:
        break
    if event == 'Select':
        filename = values['File']
        if os.path.exists(filename):
            image = Image.open(values['File'])  
            image.thumbnail((600,600))
            image.save('tranfer_image.png')
            rotate(rotate_values_image)
            process_image('tranfer_image.png')
    if event == 'Clear':
        try:
            window['SImage'].update()
        except:
            sg.popup('Error')    
    if values['_gray'] == True and event == 'Select':
        try:
            gray_image()
            rotate(rotate_values_image)
            process_image('tranfer_image.png')
        except:
            sg.popup('Error')
    if values['_blur'] == True and event == 'Select':
        try:
            blur_image()
            rotate(rotate_values_image)
            process_image('tranfer_image.png')
        except:
            sg.popup('Error')
    if values['_blur'] == True and values['_gray']== True and event == 'Select':
        try:
            BlurAGray_image()
            rotate(rotate_values_image)
            process_image('tranfer_image.png')
        except:
            sg.popup('Error')
    
    if values['_emboss'] == True:
        try:
            Emboss()
            rotate(rotate_values_image)
            process_image('tranfer_image.png')
            if values['_emboss'] == True and values['_blur'] == True and values['_gray'] == False:
                BlurEmboss()
                rotate(rotate_values_image)
                process_image('tranfer_image.png')
        except:
            sg.popup('Error')
    
    if values['_mirror'] == True:
        try:
            flip_image(1)
            rotate(rotate_values_image)
            if values['_mirror'] == True and values['_blur'] == True:
                flip_image(2)
                rotate(rotate_values_image)
            if values['_mirror'] == True and values['_gray'] == True:
                flip_image(3)
                rotate(rotate_values_image)
            if values['_mirror'] == True and values['_gray'] == True and values['_blur'] == True:
                flip_image(4)
                rotate(rotate_values_image)
            process_image('tranfer_image.png')
        except:
            sg.popup('Error')
    
    if values['_mirror'] == True and values['_emboss'] == True and values['_gray'] == False:
        try:
            FlipEmboss('normalaa')
            rotate(rotate_values_image)
            process_image('tranfer_image.png')
        except:
            sg.popup('Error')
    if values['_mirror'] == True and values['_emboss'] == True and values['_blur'] == True and values['_gray'] == False:
        try:
            FlipEmboss('blur')
            rotate(rotate_values_image)
            process_image('tranfer_image.png')
        except:
            sg.popup('Error')
        
    if values['_emboss'] == True and values['_gray'] == True and values['_blur'] == False:
        sg.popup('Can\'t use gray with emboss ')
    if values['_emboss'] == True and values['_gray'] == True and values['_blur'] == True:
        sg.popup('Can\'t use gray with emboss ')
        
#safty winclose
window.close()