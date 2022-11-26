import pygame, sys 
import random 

pygame.init()
clock = pygame.time.Clock()

windowSize = (1200, 800)
window = pygame.display.set_mode((windowSize), pygame.NOFRAME, vsync=1)

particles = []
colors = [(169, 161, 216), (255, 45, 45), (255, 255, 255)]

class Particle():
    def __init__(self, x, y, dx, dy, radius, color, g=None):
        self.x = x 
        self.y = y
        self.dx = dx 
        self.dy = dy 
        self.g = g 
        self.radius = radius 
        self.color = color

    def render(self, window):
        self.x += self.dx 
        self.y += self.dy 

        if self.g is not None:
            self.dy += self.g

        self.radius -= 0.1 
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

def show():
    for particle in particles:
        particle.render(window) 
        if particle.radius <= 0:
            particles.remove(particle)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for i in range(random.randint(15, 25)):
        particle = Particle(pos[0], pos[1], random.randint(0, 20)/10, random.randint(-3, -1), random.randint(2,5), random.choice(colors), 0.5)
        particles.append(particle)

    window.fill((0,0,0))
    show()
    pygame.display.update()