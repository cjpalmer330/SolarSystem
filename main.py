import os.path
import pygame
import math
import random

## initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("<Your game>")
clock = pygame.time.Clock()  ## For syncing the FPS
pauseBut = pygame.transform.scale_by(pygame.image.load('pause-button-svgrepo-com.svg'), 0.1)
playBut = pygame.transform.scale_by(pygame.image.load('play-button-svgrepo-com.svg'),0.1)
pauseState = False
running = True
FPS = 240
mousePos = pygame.mouse.get_pos()

class Slider:
    def __init__(self, pos: tuple, size: tuple, initialPercent: float, minVal: float, maxVal: float):
        self.pos = pos
        self.size = size
        self.min = minVal
        self.max = maxVal
        self.sliderX = self.pos[0]

        # x position minus or plus half of the width size as to make the position the center point
        self.sliderLeft = self.pos[0] - (size[0] // 2)
        self.sliderRight = self.pos[0] + (size[0] // 2)
        self.sliderTop = self.pos[1] - (size[1] // 2)
        self.initialValue = (self.sliderRight - self.sliderLeft) * initialPercent

        # rects for display
        self.containerRect = pygame.Rect(self.pos[0] - (size[0] // 2), self.sliderTop, self.size[0], self.size[1])
        self.buttonRect = pygame.Rect(self.sliderX, self.sliderTop, 10, self.size[1])

    def moveSlider(self, currentMouse):
        self.buttonRect.centerx = currentMouse[0]

    def renderSlider(self):
        pygame.draw.rect(screen, '#8a8a8a', self.containerRect)
        pygame.draw.rect(screen, '#525252', self.buttonRect)

    def getValue(self):
        valRange = self.sliderRight - self.sliderLeft - 1
        buttonVal = self.buttonRect.centerx - self.sliderLeft

        return(buttonVal/valRange)*(self.max - self.min) + self.min

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

# randomized velocities for the two planet system
randBlueX = round(random.uniform(-2.3, 2.3), 4)
randBlueY = round(random.uniform(-2.3, 2.3), 4)
greenXLowerBound, greenYLowerBound = -2.5, -2.5
if randBlueX < 0:
    greenXLowerBound = 0
if randBlueY < 0:
    greenYLowerBound = 0
randGreenX = round(random.uniform(greenXLowerBound, 2.3), 4)
randGreenY = round(random.uniform(greenYLowerBound, 2.3), 4)

# declare planets
AllPlanets = [
    # planet and moons
    # planet(300, '#5555FF', 700, 500, [0, 0], 5, True),
    # planet(30, '#55FF55', 900, 500, [0, 10.7], 1, False),
    # planet(30, '#FF5577', 400, 500, [0, -9], 1, False)

    # two body system
    planet(50, "#5555FF", 500, 500, [randBlueX, randBlueY], 1, False),
    planet(50, "#55FF55", 600, 600, [randGreenX, randGreenY], 1, False)
              ]
sliderList = [
    # gravitational Constant
    Slider((1800, 100), (150, 20), 0.5, 50, 250),
    # simulation speed
    Slider((1800, 150), (150, 20), 0.0, 32, 1024),
    # trail length
    Slider((1800, 200), (150, 20), 0.5, 15, 500)
]
sliderText = [
    "Gravitational Constant",
    "Simulation Speed",
    "Orbital Trail Length",
    "Blue X Init Vel: " + str(randBlueX),
    "Blue Y Init Vel: " + str(randBlueY),
    "Green X Init Vel: " + str(randGreenX),
    "Green Y Init Vel: " + str(randGreenY)
]
while running:
    clock.tick(FPS)

    for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

    screen.fill('#000000')

    # drawing background
    screen.fill('#000000')
    randX = random.uniform(0, 1) * 1920
    randY = random.uniform(0, 1) * 1080
    # print(randX, randY)
    # drawing randomized stars
    # if j < 100:
    #    pygame.draw.polygon(screen, 'white', [(randX, randY),
    #                                         (randX + 10, randY + 2.25),
    #                                        (randX + 10 + 2.25, randY + 2.25 + 10),
    #                                       (randX + 10 + 4.5, randY + 2.25),
    #                                      (randX + 20 + 4.5, randY),
    #                                     (randX + 10 + 4.5, randY - 2.25),
    #                                    (randX + 10 + 2.25, randY - 2.25 - 10),
    #                                   (randX + 10, randY - 2.25),
    #                                  (randX, randY)
    #                                 ], 0)



    #drawing play/pause button
    if pauseState:
        pausePlay = pauseBut
    else:
        pausePlay = playBut
    screen.blit(pausePlay, (1800, 400))

    # Displaying all sliders
    for slider in sliderList:
        slider.renderSlider()
        # calculating mouse interaction
        if slider.containerRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            slider.moveSlider(pygame.mouse.get_pos())

    # getting slider values
    gravitationalConstant = sliderList[0].getValue()
    FPS = sliderList[1].getValue()
    trailLength = sliderList[2].getValue()

    # slider labels
    i = 0
    for sliderLabel in sliderText:
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        sliderTextSurface = font.render(sliderLabel, True, 'white', 'black')
        screen.blit(sliderTextSurface, (1720, (i * 50) + 108 - 36))

        i += 1


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
