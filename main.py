import pygame
import math

## initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("<Your game>")
clock = pygame.time.Clock()  ## For syncing the FPS

running = True
FPS = 240


class planet:
    def __init__(self, mass, color, posX, posY, vel, density, lock):
        self.mass = mass * density
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = mass / 4
        self.vel = vel
        self.trail = []
        self.lock = lock

    def drawPlanet(self):

        if self.lock is False:
            self.posX += self.vel[0]
            self.posY += self.vel[1]
        pygame.draw.circle(screen, self.color, (self.posX, self.posY), self.radius)
        self.trail.append((self.posX, self.posY))
        if self.trail.__len__() > 1.5 * FPS:
            del self.trail[0]
        for trailDot in self.trail:
            pygame.draw.circle(screen, self.color, trailDot, 2)


# declare planets
gravitationalConstant = 200
AllPlanets = [planet(300, '#5555FF', 700, 500, [0, 0], 3, True),
              planet(30, '#55FF55', 900, 500, [0, 20], 1, False),
              planet(30, '#FF5577', 300, 500, [0, -17], 1, False)]
while running:
    clock.tick(FPS)

    for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

    screen.fill('#000000')

    # calculating gravity between planets
    for body in AllPlanets:
        for otherbody in AllPlanets:
            if body is otherbody:
                continue
            force = gravitationalConstant * body.mass * otherbody.mass / (
                        ((otherbody.posY - body.posY) ** 2 + (otherbody.posX - body.posX) ** 2) + 1)

            # depending on current velocity push that vector in direction of the other planet by calculated amount
            yDirection, xDirection = 1, 1
            if otherbody.posY > body.posY:
                yDirection = -1
            if otherbody.posX > body.posX:
                xDirection = -1
            if otherbody.posX == body.posX:
                angle = 0
            else:
                angle = math.atan(abs((otherbody.posY - body.posY)/(otherbody.posX - body.posX)))
            print(angle, math.pi / 2, angle / (2 * math.pi))

            # x and y ratio of the forces
            ratio = angle / (math.pi / 2)
            yForce = force * ratio
            xForce = force - yForce

            # acceleration
            otherAccelerationX = xForce / otherbody.mass * xDirection
            otherAccelerationY = yForce / otherbody.mass * yDirection
            # if moving away from the body, negative acceleration
            if otherbody.posX > body.posX:
                lol = 1
            otherbody.vel[0] += otherAccelerationX / (FPS / 60)
            otherbody.vel[1] += otherAccelerationY / (FPS / 60)
            print(force, xForce, yForce, "forces, ratio:", ratio)

    for body in AllPlanets:
        body.drawPlanet()
    # gravity equation
    # force = bigG * mass

    ## Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
