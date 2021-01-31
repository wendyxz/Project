
import os


'''FPS'''
FPS = 40
'''Game Screen Size'''
SCREENSIZE = (640, 640)
'''Picture Path'''
SKIER_IMAGE_PATHS = [
    os.path.join(os.getcwd(), 'resources/images/skier_forward.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_right1.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_right2.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_left2.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_left1.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_fall.png')
]
OBSTACLE_PATHS = {
    'tree': os.path.join(os.getcwd(), 'resources/images/tree.png'),
    'flag': os.path.join(os.getcwd(), 'resources/images/flag.png')
}

'''Font Path'''
FONTPATH = os.path.join(os.getcwd(), 'resources/font/FZSTK.TTF')
