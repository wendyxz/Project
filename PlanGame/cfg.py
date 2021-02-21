'''Configuration File'''
import os


'''Screen Size'''
SCREENSIZE = (956, 560)
'''Font Path'''
FONTPATH = os.path.join(os.getcwd(), 'resources/font/simkai.ttf')
'''Image Paths'''
IMAGEPATHS = {
    'asteroid': os.path.join(os.getcwd(), 'resources/images/asteroid2.png'),
    'bg_big': os.path.join(os.getcwd(), 'resources/images/bg_big.png'),
    'bullet': os.path.join(os.getcwd(), 'resources/images/bullet.png'),
    'seamless_space': os.path.join(os.getcwd(), 'resources/images/seamless_space.png'),
    'ship': os.path.join(os.getcwd(), 'resources/images/ship3.png'),
    'ship_exploded': os.path.join(os.getcwd(), 'resources/images/ship_exploded.png'),
    'space3': os.path.join(os.getcwd(), 'resources/images/space3.jpg'),
}
'''Sound Paths'''
SOUNDPATHS = {
    'boom': os.path.join(os.getcwd(), 'resources/sounds/boom.wav'),
    'Cool Space Music': os.path.join(os.getcwd(), 'resources/sounds/Cool Space Music.mp3'),
    'shot': os.path.join(os.getcwd(), 'resources/sounds/shot.ogg'),
}
