import pygame
import settings

pygame.joystick.init()

num_joysticks = pygame.joystick.get_count()

p1_controller = None
p2_controller = None

if num_joysticks == 1:
    p1_controller = pygame.joystick.Joystick(0)
    p1_controller.init()
    print("Player 1 controller connected:", p1_controller.get_name())
elif num_joysticks == 2:
    p1_controller = pygame.joystick.Joystick(0)
    p1_controller.init()
    p2_controller = pygame.joystick.Joystick(1)
    p2_controller.init()
    print(f"Player 1 controller connected: {p1_controller.get_name()} - Player 2 controller connected: {p2_controller.get_name()}")
else:
    print("No controller detected.")