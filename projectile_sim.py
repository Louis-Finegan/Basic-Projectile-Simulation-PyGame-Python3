
# Libaries used
import pygame
from math import *
import time
import os

# RGB COLORS values are stored in a dictionary with their corrisponding name
COLORS = {
    'WHITE': (255, 255, 255),
    'GREY': (127, 127, 127),
    'LIGHT_GREY': (200, 200, 200),
    'RED': (225, 0, 0),
    'BLACK': (0, 0, 0)
}

# Coefficent of restitution
c = 0.95

# Class for the ball object
class ball:
    def __init__(self, start_vel, angle):
        self.start_vel = start_vel
        self.angle = angle
        self.dt = 0.01
        self.BALL_ICON = pygame.image.load(os.path.join('icons', 'icons8-ball-64.png'))
        self.BALL = pygame.transform.scale(self.BALL_ICON, (32, 32))

    # Sets initial velocity
    def init_vel(self):
        vel_x = self.start_vel[0] * cos(radians(self.angle))
        vel_y = -self.start_vel[1] * sin(radians(self.angle))

        return vel_x, vel_y

    # Draw ball icon
    def draw_ball(self, SCREEN, pos):  
        SCREEN.fill(COLORS['WHITE'])
        SCREEN.blit(self.BALL, pos)
        pygame.display.update()  

    # Gets ball width
    def width_ball(self):
        return self.BALL.get_width()

    # Gets ball height
    def height_ball(self):
        return self.BALL.get_height()

# Class for the input rectangles
class input_rect:
    def __init__(self, locs, col_passive, col_active):
        self.locs = locs
        self.col_passive = col_passive
        self.col_active = col_active
        self.color_active = pygame.Color(col_active)
        self.color_passive = pygame.Color(col_passive)
        self.base_font = pygame.font.Font(os.path.join('fonts', 'arial.ttf'), 24)
        self.user_text = ''

    def draw_rect(self):
        rect = pygame.Rect(self.locs[0], self.locs[1], 128, 32)
        return rect

    def render_text(self, SCREEN):
        text_surface = self.base_font.render(self.user_text, True, COLORS['RED'])
            
        # render at position stated in arguments
        SCREEN.blit(text_surface, (self.draw_rect().x+5, self.draw_rect().y+5))
            
        # set width of textfield so that text cannot get
        # outside of user's text input
        self.draw_rect().w = max(100, text_surface.get_width()+3)

        pygame.display.flip()
  
    def width_rect(self):
        return self.draw_rect().width
    
    def height_rect(self):
        return self.draw_rect().height

def main():
    # Initialize Pygame
    pygame.init()
    SIZE = (900, 700)
    SCREEN = pygame.display.set_mode(SIZE)
    SCREEN.fill(COLORS['WHITE'])
    pygame.display.flip()
    ICON = pygame.image.load(os.path.join('icons', 'icons8-catapult-50.png')) # icon in the GUI
    pygame.display.set_icon(ICON)                                             # Sets the image
    clock = pygame.time.Clock()

    GRAVITATIONAL_ACCELERATION = 980

    # Creates the input boxes
    boxes = [input_rect([SIZE[0]/2 - 128/2, SIZE[1]/2 - 40], COLORS['GREY'], COLORS['LIGHT_GREY']),
        input_rect([SIZE[0]/2 - 128/2, SIZE[1]/2 + 0], COLORS['GREY'], COLORS['LIGHT_GREY']),
        input_rect([SIZE[0]/2 - 128/2, SIZE[1]/2 + 40], COLORS['GREY'], COLORS['LIGHT_GREY'])]
    
    color = [boxes[i].color_passive for i, _ in enumerate(boxes)]

    input_box = [boxes[i].draw_rect() for i, _ in enumerate(boxes)]

    # Initial States the simulation is set
    running = True
    pressed_return = False
    active = [False, False, False]

    # Initialize timer
    timer = time.time()

    # Start the game loop
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                
                # Press q to quit
                if event.key == pygame.K_q:
                    running = False

                # press r to reset
                if event.key == pygame.K_r:
                    running = False
                    main()

                # Press return to start simulation would reset if incorrect 
                # parameters are input in the input boxes
                if event.key == pygame.K_RETURN:
                    pressed_return = True

                # Check for backspace
                # get text input from 0 to -1 i.e. end.
                if event.key == pygame.K_BACKSPACE and active[0]:
                    boxes[0].user_text = boxes[0].user_text[:-1]
  
                # Unicode standard is used for string
                # formation
                elif active[0]:
                    boxes[0].user_text += event.unicode

                if event.key == pygame.K_BACKSPACE and active[1]:
                    boxes[1].user_text = boxes[1].user_text[:-1]

                elif active[1]:
                    boxes[1].user_text += event.unicode

                if event.key == pygame.K_BACKSPACE and active[2]:
                    boxes[2].user_text = boxes[2].user_text[:-1]

                elif active[2]:
                    boxes[2].user_text += event.unicode

                # Use up_key or down_key to switch between input boxes
                if event.key == pygame.K_DOWN:
                    if active[0]:
                        active = [False, True, False]

                    elif active[1]:
                        active = [False, False, True]

                    elif active[2]:
                        active = [True, False, False]

                if event.key == pygame.K_UP:
                    if active[0]:
                        active = [False, False, True]

                    elif active[1]:
                        active = [True, False, False]

                    elif active[2]:
                        active = [False, True, False]

            # Sets the box to active when clicked on
            if event.type == pygame.MOUSEBUTTONDOWN:

                # For box 1
                if input_box[0].collidepoint(event.pos):
                    active[0] = True
                else:
                    active[0] = False

                # For box 2
                if input_box[1].collidepoint(event.pos):
                    active[1] = True
                else:
                    active[1] = False

                # For box 3   
                if input_box[2].collidepoint(event.pos):
                    active[2] = True
                else:
                    active[2] = False

        # Change color of the selected input box and renders text in the selected box
        # Once the return key is pressed the boxes disappear
        if not pressed_return:
            for i, box in enumerate(boxes):
                if active[i]:
                    color[i] = box.color_active
                else:
                    color[i] = box.color_passive

                pygame.draw.rect(SCREEN, color[i], input_box[i])
                box.render_text(SCREEN)

            if boxes[0].user_text != '' and boxes[1].user_text != '' and boxes[2].user_text != '':
                try:
                    # Creates the object ball
                    obj = ball([float(boxes[0].user_text)*100, float(boxes[1].user_text)*100], float(boxes[2].user_text))

                    # Set the initial position of the projectile
                    pos_x = 10
                    pos_y = SIZE[1] - obj.height_ball()

                    # Calculate the initial velocity components in x and y
                    vel_x, vel_y = obj.init_vel()
                    
                except ValueError:
                    running = False
                    main()

        # If enter key is pressed simulation will begin
        if pressed_return:  

            try:
                # Update the position of the projectile
                pos_x += vel_x * obj.dt
                pos_y += vel_y * obj.dt
                vel_y += GRAVITATIONAL_ACCELERATION * obj.dt

                # Check if the projectile has hit the boundaries of the display
                if pos_y > SIZE[1] - obj.height_ball():
                    vel_y = - c*vel_y
                    pos_y = SIZE[1] - obj.height_ball()

                if pos_y < 0:
                    vel_y = - c*vel_y
                    pos_y = 0

                if pos_x > SIZE[0] - obj.width_ball():
                    vel_x = - c*vel_x
                    pos_x = SIZE[0] - obj.width_ball()

                if pos_x < 0:
                    vel_x = - c*vel_x
                    pos_x = 0

                # Stop simulation when ball in stationary in both x and y
                # directions
                if vel_x == 0 or vel_y == 0:
                    running = False

                # After approx 60 seconds simulation will stop and window close
                # Exiting the program
                if time.time() - timer >= 60:
                    running = False

                # Draw the projectile
                obj.draw_ball(SCREEN, (pos_x, pos_y))
                
                # Update the SCREEN
                pygame.display.update()

            # Handles incorrect inputs in the input boxes
            except UnboundLocalError:
                running = False
                main()
    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    main()