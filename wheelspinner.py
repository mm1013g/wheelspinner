import pygame, sys, os
import math

class Circle:
    def __init__(self, x, y, color, radius, width=0):
        # Circle Vars
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.radius = radius

        # Line Vars
        self.line_angle = 0
        self.line_len = 50
        self.line_start = [int(self.x + self.radius * math.cos(self.line_angle)), int(self.y + self.radius * math.sin(self.line_angle))]
        self.line_end = [int(self.x + (self.radius + self.line_len) * math.cos(self.line_angle)), int(self.y + (self.radius + self.line_len) * math.sin(self.line_angle))]

        self.gravity = 10
        self.angle_deceleration = 10
        
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], int(self.radius), int(self.width))
        
        self.update_line()

        pygame.draw.line(screen, (0,0,0), self.line_start, self.line_end, 3)

    def update_line(self):
        self.line_start = [int(self.x + self.radius * math.cos(self.line_angle)), int(self.y + self.radius * math.sin(self.line_angle))]
        self.line_end = [int(self.x + (self.radius + self.line_len) * math.cos(self.line_angle)), int(self.y + (self.radius + self.line_len) * math.sin(self.line_angle))]
        # self.angle_deceleration = self.gravity * (math.sin(self.line_angle) - 1)


pygame.init()
size = width, height = 800, 800
black = (0,0,0)

screen = pygame.display.set_mode(size)

pygame.display.set_caption('Wheel Spinner')

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text, location):
    normalText = pygame.font.Font('freesansbold.ttf',35)
    TextSurf, TextRect = text_objects(text, normalText)
    TextRect.topleft = location
    screen.blit(TextSurf, TextRect)
    return TextRect


circle = Circle(width/2, height/2, (0,255,100), width/3)
screen.fill((255, 255, 255))
pygame.display.set_icon(screen)

getTicksLastFrame = 0

mouse_movement = False
mouse_pressed = False

old_angle = 0
new_angle = 0
angle_vel = 0

# Vars for counting spins
start_angle = 0
end_angle = 0

high_score = 0

done = False
while not done:
    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    
    old_angle = new_angle
    new_angle = circle.line_angle

    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
        if event.type == pygame.MOUSEBUTTONDOWN: # and not mouse_pressed:
            mouse_pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_movement = True
            mouse_pressed = False
    
    screen.fill((255, 255, 255))
    
    if mouse_movement:
        angle_vel = (new_angle - old_angle) / deltaTime
        mouse_movement = False

    if angle_vel > 0.05:
        angle_vel -= circle.angle_deceleration * deltaTime
    elif angle_vel < -0.05:
        angle_vel += circle.angle_deceleration * deltaTime
    else:
        angle_vel = 0

    circle.line_angle += angle_vel * deltaTime

    if mouse_pressed:
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - circle.x
        dy = mouse_pos[1] - circle.y
        circle.line_angle = math.atan2(dy,dx)
        start_angle = circle.line_angle
        end_angle = start_angle
    end_angle = circle.line_angle
    angle_change = math.fabs(start_angle - end_angle)
    
    rotations = angle_change / (2 * math.pi)
    high_score = rotations if rotations > high_score else high_score
    
    rotate_message = message_display(f'Rotations: {rotations:.3f}', (0, 0))
    high_score_message = message_display(f'High Score: {high_score:.3f}', rotate_message.bottomleft)
    vel_message = message_display(f'Angular Velocity: {angle_vel:.3f}', high_score_message.bottomleft)

    circle.draw(screen)
    pygame.display.flip()

pygame.quit()