
import configparser
import utilities

config = configparser.ConfigParser()
try:
    config.read(utilities.resource_path('settings.ini'))
    config['SCREEN']['FPS']

    FPS = int(config['SCREEN']['FPS'])
    SCREEN_WIDTH = int(config['SCREEN']['SCREEN_WIDTH'])
    SCREEN_HEIGHT = int(config['SCREEN']['SCREEN_HEIGHT'])

    SCALE = (SCREEN_WIDTH + SCREEN_HEIGHT) / 1400
except Exception as e:
    print("Error: ", e)