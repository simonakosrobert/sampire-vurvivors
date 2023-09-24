
import configparser

config = configparser.ConfigParser()

config.read('settings.ini')
config['SCREEN']['FPS']

FPS = int(config['SCREEN']['FPS'])
SCREEN_WIDTH = int(config['SCREEN']['SCREEN_WIDTH'])
SCREEN_HEIGHT = int(config['SCREEN']['SCREEN_HEIGHT'])

SCALE = (SCREEN_WIDTH + SCREEN_HEIGHT) / 1400