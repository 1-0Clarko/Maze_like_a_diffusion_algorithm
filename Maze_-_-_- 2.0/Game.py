from Displey import *
import random

run = False
clock = pygame.time.Clock()
fps = 60
ViewDistance = 6
MovimentDelaySpeed = 200
AnimalsSpownAreaFromStart = 15
MinAnimals = 5
MaxAnimals = 15

class Terrein:
    def __init__(self): {}
    def SetData(self, StartSquare, GoalSquare, WalkableSquaresList, LabSize):
        self.WalkableSquaresList = WalkableSquaresList
        self.StartSquare = StartSquare
        self.GoalSquare = GoalSquare
        self.LabSize = LabSize
        self.Water = []
    def GenerateNature(self):
        self.GenerateWater()
        self.SpawnAnimals()
    def GenerateWater(self):

        N_Pools = random.randint(1,100)
        if N_Pools == 0:
            return
        for i in range(1, N_Pools):
            pos = [random.randint(0,self.LabSize), random.randint(0,self.LabSize)]
            if not (pos in self.WalkableSquaresList):
                self.GeneratePool(pos)
    def GeneratePool(self, Pos):
        NewWater = [[Pos[0], Pos[1]]]
        MaxWater = 30
        WhaterBlocks = 0
        i = 0
        while True:
            # Up
            PosPlusDir = [NewWater[i][0], NewWater[i][1]+1]
            if random.choice([True, False]):
                if not (PosPlusDir in self.WalkableSquaresList) and not (PosPlusDir in self.Water) and not (PosPlusDir in NewWater) and NewWater[i][1]<self.LabSize:
                        NewWater.append(PosPlusDir)
                        WhaterBlocks = WhaterBlocks + 1
            # Down
            PosPlusDir = [NewWater[i][0], NewWater[i][1]-1]
            if random.choice([True, False]):
                if not (PosPlusDir in self.WalkableSquaresList) and not (PosPlusDir in self.Water) and not (PosPlusDir in NewWater) and NewWater[i][1]>self.LabSize:
                        NewWater.append(PosPlusDir)
                        WhaterBlocks = WhaterBlocks + 1
            # Left
            PosPlusDir = [NewWater[i][0]+1, NewWater[i][1]]
            if random.choice([True, False]):
                if not (PosPlusDir in self.WalkableSquaresList) and not (PosPlusDir in self.Water) and not (PosPlusDir in NewWater) and NewWater[i][0]<self.LabSize:
                        NewWater.append(PosPlusDir)
                        WhaterBlocks = WhaterBlocks + 1
            # Right
            PosPlusDir = [NewWater[i][0]-1, NewWater[i][1]]
            if random.choice([True, False]):
                if not (PosPlusDir in self.WalkableSquaresList) and not (PosPlusDir in self.Water) and not (PosPlusDir in NewWater) and NewWater[i][0]>self.LabSize:
                        NewWater.append(PosPlusDir)
                        WhaterBlocks = WhaterBlocks + 1
            #print(NewWater)
            i += 1
            if (i == len(NewWater) or WhaterBlocks == MaxWater):
                break
            #WaitA_Click()
        self.Water.extend(NewWater)
    def SpawnAnimals(self):
        Animals.clear()
        num_water = random.randint(3, 6)
        for _ in range(num_water):
            MaxTry = 25
            Try = 0
            while True:
                Water = random.choice(self.Water)
                pos = [Water[0] + random.randint(-AnimalsSpownAreaFromStart, AnimalsSpownAreaFromStart), Water[1] + random.randint(-AnimalsSpownAreaFromStart, AnimalsSpownAreaFromStart)]
                if pos in self.WalkableSquaresList:
                    Try = 0
                    Animals.append(NPC("g", pos))
                    break
                Try += 1
                if Try == MaxTry:
                    break
        num_animals = random.randint(int(MinAnimals*0.3), int(MaxAnimals*0.3))
        for _ in range(num_animals):
            MaxTry = 25
            Try = 0
            while True:
                pos = [self.StartSquare[0] + random.randint(-AnimalsSpownAreaFromStart, AnimalsSpownAreaFromStart), self.StartSquare[1] + random.randint(-AnimalsSpownAreaFromStart, AnimalsSpownAreaFromStart)]
                if pos in self.WalkableSquaresList:
                    Try = 0
                    Animals.append(NPC("g", pos))
                    break
                Try += 1
                if Try == MaxTry:
                    break
        print("Ci sono:", len(Animals), " animali")



class Player:
    def __init__(self):
        self.Health = Health(100, self.TakeDameg, self.Death)
        self.PriviusImputTime = 0
        self.MoveUp = False
        self.MoveDown = False
        self.MoveLeft = False
        self.MoveRigt = False
        self.Inventory = {}
    def Set(self, pos, image):
        self.pos = pos
        self.image = image
        self.angle = 0
    def UpdateImput(self, event, Up):
        self.PriviusImputTime = pygame.time.get_ticks()
        if not Up:
            if event.key == pygame.K_w:
                self.MoveUp = True
                self.MoveDown = False
            elif event.key == pygame.K_a:
                self.MoveLeft = True
                self.MoveRigt = False
            elif event.key == pygame.K_s:
                self.MoveUp = False
                self.MoveDown = True
            elif event.key == pygame.K_d:
                self.MoveRigt = True
                self.MoveLeft = False
            elif event.key == 13:
                self.Attack()
            
            self.UpdateMoviment()
        else:
            if event.key == pygame.K_w:
                self.MoveUp = False
            elif event.key == pygame.K_a:
                self.MoveLeft = False
            elif event.key == pygame.K_s:
                self.MoveDown = False
            elif event.key == pygame.K_d:
                self.MoveRigt = False
    def UpdateMoviment(self):
        nextPos = self.pos.copy()
        if self.MoveUp and not self.MoveLeft and not self.MoveRigt:
            nextPos[1] += -1
            self.angle = 180
        if self.MoveUp and self.MoveLeft:
            nextPos[1] += -1
            nextPos[0] += -1
            self.angle = -135
        if self.MoveUp and self.MoveRigt:
            nextPos[1] += -1
            nextPos[0] += 1
            self.angle = 135
        if self.MoveLeft and not self.MoveUp and not self.MoveDown:
            nextPos[0] += -1
            self.angle = -90
        if self.MoveRigt and not self.MoveUp and not self.MoveDown:
            nextPos[0] += 1
            self.angle = 90
        if self.MoveDown and not self.MoveLeft and not self.MoveRigt:
            self.angle = 0
            nextPos[1] += 1
        if self.MoveDown and self.MoveLeft:
            nextPos[1] += 1
            nextPos[0] += -1
            self.angle = -45
        if self.MoveDown and self.MoveRigt:
            nextPos[1] += 1
            nextPos[0] += 1
            self.angle = 45
        if nextPos != self.pos and nextPos in TheTerrein.WalkableSquaresList:
            UdateCamerOffset([nextPos[0] - self.pos[0], nextPos[1] - self.pos[1]])
            self.pos = nextPos
            pygame.mixer.Sound.play(GrassStepSaund)
        else:
            UdateCamerOffset([0, 0])

    def Attack(self):
        Punch(self)
    def TakeDameg(self):
        None
    def Death(self):
        None
    def AddItemToInventory(self, ItemName):
        if ItemName in self.Inventory:
            self.Inventory[ItemName] += 1
        else:
            self.Inventory[ItemName] = 1
    def Update(self):
        if pygame.time.get_ticks() - self.PriviusImputTime > MovimentDelaySpeed:
            self.UpdateMoviment()
            self.PriviusImputTime = pygame.time.get_ticks()
class NPC:
    def __init__(self, Type, pos):
        self.MoveUp = False
        self.MoveDown = False
        self.MoveLeft = False
        self.MoveRight = False
        print(self, Type, pos)
        self.Type = Type
        self.pos = pos
        self.angle = random.choice([0,180,-135, 135, -90, 90, -45, 45])
        if (Type == "g"):
            self.image = chickenImg
            self.Health = Health(20, self.TakeDameg, self.Death)
        if (Type == "l"):
            self.image = PitcherImg[0]
            self.AnimationState = 0
            self.Health = Health(20, self.TakeDameg, self.Death)
        self.PriviusImputTime = pygame.time.get_ticks()
    def UpdateMoviment(self):
        nextPos = self.pos.copy()
        if (self.Type == "g"):
            GoVertcal = random.randint(-1, 1)
            GoHorizontal = random.randint(-1, 1)
            if GoVertcal == 1:
                self.MoveUp = True
            elif GoVertcal == 0:
                self.MoveUp = False
                self.MoveDown = False
            elif  GoVertcal == -1:
                self.MoveDown = True

            if GoHorizontal == 1:
                self.MoveRight = True
            elif GoHorizontal == 0:
                self.MoveRight = False
                self.MoveLeft = False
            elif  GoHorizontal == -1:
                self.MoveLeft = True
        
        if self.MoveUp and not self.MoveLeft and not self.MoveRight:
            nextPos[1] += -1
            self.angle = 180
        if self.MoveUp and self.MoveLeft:
            nextPos[1] += -1
            nextPos[0] += -1
            self.angle = -135
        if self.MoveUp and self.MoveRight:
            nextPos[1] += -1
            nextPos[0] += 1
            self.angle = 135
        if self.MoveLeft and not self.MoveUp and not self.MoveDown:
            nextPos[0] += -1
            self.angle = -90
        if self.MoveRight and not self.MoveUp and not self.MoveDown:
            nextPos[0] += 1
            self.angle = 90
        if self.MoveDown and not self.MoveLeft and not self.MoveRight:
            self.angle = 0
            nextPos[1] += 1
        if self.MoveDown and self.MoveLeft:
            nextPos[1] += 1
            nextPos[0] += -1
            self.angle = -45
        if self.MoveDown and self.MoveRight:
            nextPos[1] += 1
            nextPos[0] += 1
            self.angle = 45
        if nextPos != self.pos and nextPos in TheTerrein.WalkableSquaresList:
            self.pos = nextPos
            PlayDistanceEffectedAudio(GrassStepSaund, self.pos, ThePlayer.pos, 0.4)
    def Death(self):
        if self.Type == "g":
            print("Chicken dead")
            pygame.mixer.Sound.play(ChickenDead)
            ThePlayer.AddItemToInventory("Chicken")

    def TakeDameg(self):
        if self.Type == "g":
            pygame.mixer.Sound.play(random.choice(ChickenHurtSounds))
    def Update(self):
        if not self.Health.Alive:
            return
        if pygame.time.get_ticks() - self.PriviusImputTime > MovimentDelaySpeed:
            self.UpdateMoviment()
            self.PriviusImputTime = pygame.time.get_ticks()
        if (self.Type == "l"):
            if pygame.time.get_ticks() - self.PriviusImputTime > MovimentDelaySpeed*2:
                Go = random.randint(1, 4)
                self.MoveUp = False
                self.MoveDown = False
                self.MoveRight = False
                self.MoveLeft = False
                match Go:
                    case 1:
                        self.MoveUp = True
                    case 2:
                        self.MoveDown = True
                    case 3:
                        self.MoveLeft = True
                    case 4:
                        self.MoveRight = True
                if self.AnimationState == 0:
                    self.AnimationState = 1
                if self.AnimationState == 1:
                    self.AnimationState = 0
                self.PriviusImputTime = pygame.time.get_ticks()
class Health:
    def __init__(self, MaxHealth, HurtFunction, DethFunction):
        self.MaxHealth = MaxHealth
        self.Health = MaxHealth
        self.HurtFunction = HurtFunction
        self.DethFunction = DethFunction
        self.Alive = True
    def TakeDameg(self, Dameg):
        if self.Alive == False:
            return
        print("Preso Danno",Dameg)
        self.Health = self.Health - Dameg
        if self.Health <= 0:
            self.DethFunction()
            self.Alive = False
        else:
            self.HurtFunction()
Animals = []
Monsters = []
ThePlayer = Player()
TheTerrein = Terrein()
def StartLoop(StartSquare, GoalSquare, WalkableSquaresList, LabSize):
    global run  # Dichiarazione che 'run' è una variabile globale
    run = True

    TheTerrein.SetData(StartSquare, GoalSquare, WalkableSquaresList, LabSize)
    ThePlayer.Set(StartSquare.copy(), random.choices(PlayerCharacters)[0])    
    TheTerrein.GenerateNature()
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                ThePlayer.UpdateImput(event, False)
            if event.type == pygame.KEYUP:
                ThePlayer.UpdateImput(event, True)

        screen.fill((201,79,91))
        ThePlayer.Update()
        for Animal in Animals:
            Animal.Update()
        for Moster in Monsters:
            Moster.Update()
        VisualaizeTerrein()
        VisualizeCharacters()
        
        VisualizeInventory()
        global FramesWater
        FramesWater = FramesWater + 1
        if FramesWater > MaxFramesWater-1:
            FramesWater = 0
        UpdateDisplay()
    Quit()

def VisualaizeTerrein():
    for x in range(-ViewDistance, ViewDistance):
        for y in range(-ViewDistance, ViewDistance):
            if (ControllaSeE_NelRaggioVisivo((x, y))):
                Pos_List = [ThePlayer.pos[0] + x, ThePlayer.pos[1] + y]

                if Pos_List == TheTerrein.StartSquare:
                    display_image_Squere(x+ViewDistance, y+ViewDistance, Start, 60, 60)
                elif Pos_List in TheTerrein.WalkableSquaresList:
                    display_image_Squere(x+ViewDistance, y+ViewDistance, Grass, 60, 60)
                elif Pos_List in TheTerrein.Water:
                    display_image_Squere(x+ViewDistance, y+ViewDistance, WaterImages[FramesWater], 60, 60)
                elif Pos_List == TheTerrein.GoalSquare:
                    display_image_Squere(x+ViewDistance, y+ViewDistance, Demon, 60, 60, 100, True, RenderHierarchy=1)
                else:
                    display_image_Squere(x+ViewDistance, y+ViewDistance, Rook, 60, 60, 10)
def VisualizeCharacters():
    for NPC in Animals + Monsters:
        Difference = [0, 0]
        Difference[0] = ThePlayer.pos[0] - NPC.pos[0]
        Difference[1] = ThePlayer.pos[1] - NPC.pos[1]
        if ControllaSeE_NelRaggioVisivo([-Difference[0], -Difference[1]]):
            if not type(NPC) is list:
                image = NPC.image
            else:
                image = NPC.image[NPC.AnimationState]
            display_image_Squere(-Difference[0]+ViewDistance, -Difference[1]+ViewDistance, image, 60, 60, 50, True, angle=NPC.angle)

    display_image(DisplayWidth/2-65, DisplayHeight/2-65, ThePlayer.image, 100, 100, ThePlayer.angle)
def VisualizeInventory():
    for i in range(len(ThePlayer.Inventory)):
        ItemName = list(ThePlayer.Inventory.keys())[i]
        DrawText(ItemName+" x"+str(ThePlayer.Inventory[ItemName]), BegningFont, (255, 255, 255), 30, 30, Display=False)

def ControllaSeE_NelRaggioVisivo(pos):
    h = 0
    D = pow(pow(pos[0]-h,2) + pow(pos[1]-h,2),1/2)
    if (D < ViewDistance):
        return True
    else:
        return False

def BuildingSound():
    pygame.mixer.Sound.play(random.choices(BuildingsSounds)[0])

def Punch(Attacker):
    for animal in Animals:
        if animal.pos == Attacker.pos:
            animal.Health.TakeDameg(10)
    display_particle(DisplayWidth/2-20, DisplayHeight/2-20, random.choices(HumanPunchesEffects)[0], 100, 35, -ThePlayer.angle, 100)
    pygame.mixer.Sound.play(random.choices(PunchesInAirSounds)[0])

def GameInit():
    pygame.init()
def Disolvence():
    fade_start_time = pygame.time.get_ticks()
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    while True:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - fade_start_time
        fade_alpha = elapsed_time*0.01
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        UpdateDisplay()
        if fade_alpha == 7:
            break

def WaitA_Click():
    HasBeenDown = False
    while (True):
        clock.tick(fps)
        for event in pygame.event.get(): {}              
        if (not pygame.mouse.get_pressed()[0]):
            HasBeenDown = True

        if pygame.mouse.get_pressed()[0] and HasBeenDown == True:
            print("Pressed")            
            return pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
def Quit():
    pygame.quit()