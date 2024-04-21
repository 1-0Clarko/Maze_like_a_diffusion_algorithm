import pygame
import sys

DisplayWidth = 800
DisplayHeight = 800
PixelsPerSquare = 0
MaxHearingRange = 13

RenderHierarchys = []
Particles = []

CameraMovementInFrame = []
UpdateMoviment = False

pygame.font.init()
pygame.mixer.init()
BegningFont = pygame.font.SysFont("img\Vertically.otf", 30)

screen = pygame.display.set_mode((DisplayWidth, DisplayHeight))
Rook = pygame.image.load("img\Rook1.png")
Grass = pygame.image.load("img\Grass.png")
Start = pygame.image.load("img\Start.png")
Demon = pygame.image.load("img\Goal.png")
PunchSound = pygame.mixer.Sound("Sounds/Punch.wav")
ChickenDead = pygame.mixer.Sound("Sounds/ChickenKiled.mp3")

chickenImg = pygame.image.load("img\chicken.png")

PitcherImg = [
    pygame.image.load("img\Lancatore1.png"),
    pygame.image.load("img\Lancatore2.png"),
    pygame.image.load("img\LancatoreLanco1.png"),
    pygame.image.load("img\LancatoreLanco2.png")
]  
ChickenHurtSounds = [
    pygame.mixer.Sound("Sounds/ChickenHurt1.wav"),
    pygame.mixer.Sound("Sounds/ChickenHurt2.wav"),
    pygame.mixer.Sound("Sounds/ChickenHurt3.wav"),
    pygame.mixer.Sound("Sounds/ChickenHurt4.wav"),
    pygame.mixer.Sound("Sounds/ChickenHurt5.wav"),
]
HumanPunchesEffects = [
    pygame.image.load("img\PugnioUmano1.png"),
    pygame.image.load("img\PugnioUmano2.png"),
    pygame.image.load("img\PugnioUmano3.png")
]
PunchesInAirSounds = [
    pygame.mixer.Sound("Sounds/punchInAir1.mp3"),
    pygame.mixer.Sound("Sounds/punchInAir2.mp3"),
    pygame.mixer.Sound("Sounds/punchInAir3.mp3")
]
BuildingsSounds = [
    pygame.mixer.Sound("Sounds/LegoBuild1.wav"),
    pygame.mixer.Sound("Sounds/LegoBuild3.wav"),
    pygame.mixer.Sound("Sounds/LegoBuild4.wav"),
    pygame.mixer.Sound("Sounds/LegoBuild5.wav"),
    pygame.mixer.Sound("Sounds/LegoBuild6.wav"),
    pygame.mixer.Sound("Sounds/LegoBuild7.wav")
]
GrassStepSaund = pygame.mixer.Sound("Sounds/Step.mp3")

PlayerCharacters = [
    pygame.image.load("img\Parsonaggio1.png"),
    pygame.image.load("img\Parsonaggio2.png"),
    pygame.image.load("img\Parsonaggio3.png"),
    pygame.image.load("img\Parsonaggio4.png")
]

MaxFramesWater = 39
FramesWater = 0
WaterImages = []
for i in range(39):
    Num = f"{i:04}"
    WaterImages.append(pygame.image.load(f"img\Water\{Num}.png"))

def StartDisplay(PixelsXSquare): #run at the very start
    global PixelsPerSquare
    PixelsPerSquare = PixelsXSquare
    pygame.display.set_caption('Maze like a function collapse')
    return

def display_square(x, y, color, pixel_for_square, Display = True):
    x, y = x * pixel_for_square, y * pixel_for_square

    pygame.draw.rect(screen, color, pygame.Rect(x, y, pixel_for_square, pixel_for_square))
    if (Display):
        UpdateDisplay()

    return
def display_small_square(x, y, color, pixel_for_square_big, pixel_for_square_smoll):
    #x, y = x * pixel_for_square_big, y * pixel_for_square_big

    #pygame.draw.rect(screen, color, pygame.Rect(x, y, pixel_for_square_smoll, pixel_for_square_smoll))
    #UpdateDisplay()

    return
def display_image_Squere(x, y, image, Width, Height, ExtaScale = 0, Center = False, RenderHierarchy = 0, angle = 0):
    if RenderHierarchy > 0:
        RenderHierarchys.append([x, y, image, Width, Height, ExtaScale, Center, RenderHierarchy])
        return
    x, y = x * Width, y * Height
    trasformed_image = pygame.transform.scale(image, (Width+ExtaScale, Height+ExtaScale))
    if angle != 0:
        trasformed_image = pygame.transform.rotate(trasformed_image, angle)
    if RenderHierarchy == 0:
        if Center:
            screen.blit(trasformed_image, (x-ExtaScale/2, y-ExtaScale/2))
        else:
            screen.blit(trasformed_image, (x-ExtaScale, y-ExtaScale))

def display_image(x, y, image, Width, Height, angle = 0):
    trasformed_image = pygame.transform.scale(image, (Width, Height))
    if angle != 0:
        trasformed_image = pygame.transform.rotate(trasformed_image, angle)
    screen.blit(trasformed_image, (x, y))

def display_particle(x, y, image, Width, Height, rotation, time):
    StartTime = pygame.time.get_ticks()
    Particles.append([x, y, image, Width, Height, rotation, StartTime, time])

def UpdateDisplay():
    RenderHierarchys.sort(key=lambda x: x[7])
    for i in range(len(RenderHierarchys)):
        RenderHierarchys[i][7] = 0
        display_image_Squere(*RenderHierarchys[i])
    RenderHierarchys.clear()
    for Particle in Particles:
        global UpdateMoviment
        if (UpdateMoviment):
            global PixelsPerSquare
            global CameraMovementInFrame
            UpdateMoviment = False
            Particle[0] = Particle[0] + CameraMovementInFrame[0]*-PixelsPerSquare
            Particle[1] = Particle[1] + CameraMovementInFrame[1]*-PixelsPerSquare
        display_image(Particle[0], Particle[1], Particle[2], Particle[3], Particle[4], Particle[5])
        if (pygame.time.get_ticks() - Particle[6] > Particle[7]):
            Particles.remove(Particle)
    pygame.display.update()


def DrawText(text, font, text_col, x, y, Display = True):
    if Display:
        screen.fill((0, 0, 0))
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    if Display:
        UpdateDisplay()
    
def PlayDistanceEffectedAudio(Sound, pos1, pos2, Mult = 1.0):
    Distance = pow(pow((pos2[0] - pos1[0]), 2) + pow((pos2[1] - pos1[1]), 2), 1/2)
    Volume = max(-Distance + MaxHearingRange, 0)
    Volume = Volume / MaxHearingRange
    sound = pygame.mixer.Sound(Sound)
    sound.set_volume(Volume * Mult)
    sound.play()

def UdateCamerOffset(Movment):
    global CameraMovementInFrame
    global UpdateMoviment
    CameraMovementInFrame = Movment
    UpdateMoviment = True
    