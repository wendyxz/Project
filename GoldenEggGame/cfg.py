'''Configuration file'''
import os


'''Image Path'''
IMAGE_PATHS = {
    'egg': os.path.join(os.getcwd(), 'resources/images/egg.png'),
    'love': os.path.join(os.getcwd(), 'resources/images/love.png'),
    'background': os.path.join(os.getcwd(), 'resources/images/background.jpg'),
    'hero': [os.path.join(os.getcwd(), 'resources/images/%d.png' % i) for i in range(1, 11)],
}
'''Audio path'''
AUDIO_PATHS = {
    'bgm': os.path.join(os.getcwd(), 'resources/audios/bgm.mp3'),
    'get': os.path.join(os.getcwd(), 'resources/audios/get.wav'),
}
'''Font path'''
FONT_PATH = os.path.join(os.getcwd(), 'resources/font/font.TTF')
'''Path of the highest score record'''
HIGHEST_SCORE_RECORD_FILEPATH = 'highest.rec'
'''Game screen size'''
SCREENSIZE = (800, 600)
'''Background color'''
BACKGROUND_COLOR = (0, 160, 233)
'''fps'''
FPS = 30
