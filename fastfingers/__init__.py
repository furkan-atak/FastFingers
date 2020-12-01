import random
import pygame,sys


"""
WHEN YOU RUN IT,
  YOU CAN PLAY WITH UP,DOWN (DIRECTION KEYS) ON KEYBOARD 
  YOU CAN SHOOT WITH MOUSE(LEFT CLICK) AND SPACE KEY
 
"""


pygame.init()


width = 1024
height = 700

dimensions = (width,height)
window = pygame.display.set_mode(dimensions)

clock = pygame.time.Clock()

pygame.display.set_caption("FastFingers By Furkan ATAK")
theicon = pygame.image.load("theicon.png")
pygame.display.set_icon(theicon)

pygame.mixer.music.load("space.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0.0)

background = pygame.image.load("bg4.png")

meteors = ["meteor1.png","meteor2.png","meteor3.png","meteor4.png","meteor5.png"]
explosions = ["explosion5.ogg","explosion2.ogg","explosion3.ogg","explosion4.ogg"]
hitSound = ["first.ogg","DeathFlash.ogg"]
crash = ["crash1.png","crash2.png","crash3.png","crash4.png"]
ship_crash = ["ship_crash1.png","ship_crash2.png","ship_crash3.png","ship_crash4.png"]
myShip = pygame.image.load("smallShip.png")

font = pygame.font.SysFont("arial",22,True,False)
scoreFont = pygame.font.SysFont("arial",48,True,False)
level = 1
score = 0
waitingTime = True


class TheShip(pygame.sprite.Sprite):
    def __init__(self,x=width /2, y= height / 2):
        super().__init__()
        self.image = myShip.convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2) # for the circular hitbox
        self.shield = 100
        self.rect.x = 0
        self.rect.y = int(y)
        self.ship_health = 3
        self.hide_time = 1500
        self.isHide = False
        self.last_hide = pygame.time.get_ticks()

    def hide(self):
        self.isHide = True
        self.last_hide = pygame.time.get_ticks()
        self.rect.x = -200

    def update(self, *args):
        up, down, left, right = args
        if self.isHide and pygame.time.get_ticks() - self.last_hide > self.hide_time:
            self.isHide = False
            self.rect.x = 0
            self.rect.y = (window.get_size()[1]/2).__int__()

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.rect.size[1] > window.get_size()[1]:
            self.rect.y = window.get_size()[1] - self.rect.size[1]

        if up:
            self.rect.y -= 10
        if down:
            self.rect.y += 10

    def shoot(self):
        bullet = Bullets(self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bulletSound = pygame.mixer.Sound("laser1.ogg")
        bulletSound.set_volume(0.3)
        bulletSound.play()


class RandomPieces(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.chosen = random.choice(meteors)
        self.image = pygame.image.load(self.chosen).convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.7/2) # circular hitbox pieces
        self.rect.y = random.randrange(height-self.rect.height)
        self.rect.x = random.randrange(width+40,width+100)
        self.speedx = random.randrange(5,15)
        self.speedy = random.randrange(-2,2)


    def update(self,*args):
        self.rect.x -= self.speedx
        self.rect.y += self.speedy

        if self.rect.right < 0:
            self.rect.y = random.randrange(height - self.rect.height)
            self.rect.x = random.randrange(width + 40, width + 100)
            self.speedx = random.randrange(5, 15)
            self.speedy = random.randrange(-2, 2)


class Bullets(pygame.sprite.Sprite):
    def __init__(self,pieceY):
        super().__init__()
        self.image = pygame.image.load("laser.png")
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = pieceY + 30 # + 30 to supply bullets from the middle of the ship

    def update(self, *args):
        self.rect.x += 8

        if self.rect.left > width:
            self.kill()


class Crash(pygame.sprite.Sprite):
    def __init__(self,meteor,aList):
        super().__init__()
        self.meteor = meteor
        self.aList = aList
        self.index = 0
        self.image = pygame.transform.scale(pygame.image.load(self.aList[self.index]),self.meteor.image.get_size())
        self.rect = self.image.get_rect()
        self.rect.center = self.meteor.rect.center
        self.delay = 80
        self.lastChange = pygame.time.get_ticks()

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.lastChange > self.delay:
            self.lastChange = now
            self.image = pygame.transform.scale(pygame.image.load(self.aList[self.index]),self.meteor.image.get_size())
            self.rect = self.image.get_rect()
            self.rect.center = self.meteor.rect.center
            self.index += 1

        if self.index == len(self.aList):
            self.kill()

all_sprites = pygame.sprite.Group()
rndmpieces = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(15):
 rndmpiece = RandomPieces()
 all_sprites.add(rndmpiece)
 rndmpieces.add(rndmpiece)

ship1 = TheShip()
all_sprites.add(ship1)

def shieldOnscreen(window,x,y,value):
    if value < 0:
        value = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (value/100) * BAR_LENGTH
    outlineRect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    therect = pygame.Rect(x,y,fill.__int__(),BAR_HEIGHT)
    pygame.draw.rect(window,(255,255,255),outlineRect,3)
    pygame.draw.rect(window,(180,150,150),therect)

def lifeChances(x,y,lifechance):
    img = pygame.transform.scale(pygame.image.load("health1.png"),(30,30))
    img_rect = img.get_rect()
    for i in range(lifechance):
        img_rect.x = x + (40*i)
        img_rect.y = y
        window.blit(img,img_rect)


game_start = True
game_over = True

def gameStarts():
    control= True
    introScreen = pygame.image.load("entrance1.png")
    window.blit(introScreen.convert(),introScreen.get_rect())
    pygame.display.update()
    while control:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    control = False

def gameOver():
    control = True
    global score
    f = open("maxScore.txt")
    global a
    a = int(f.readline())
    if score > a:
        f.close()
        f = open("maxScore.txt","w")
        f.write(str(score))
    else:
        score = a
    outroScreen = pygame.image.load("outro3.png")
    window.blit(outroScreen.convert(),outroScreen.get_rect())
    scoreBoard = scoreFont.render("Max Score: {}".format(score), 1, (250, 250, 250))
    window.blit(scoreBoard,(window.get_size()[0] - scoreBoard.get_size()[0], window.get_size()[1] - scoreBoard.get_size()[1]))

    score = 0
    pygame.display.update()
    while control:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    control=False
                    for rndm in rndmpieces:
                        rndm.kill()
                    gameStarts()


while True:
    if game_start:
        gameStarts()
        game_start = False

    clock.tick(60)
    window.blit(background.convert(),background.get_rect())
    health = font.render("Healt of shield", 1, (250, 250, 250))
    window.blit(health,(110,5))
    shieldOnscreen(window, 5, 5, ship1.shield)
    lifeChances(5,25,ship1.ship_health)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()

        if event.type == pygame.VIDEORESIZE:
            pygame.display.init()
            pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship1.shoot()
            if event.key == pygame.K_f:
                pygame.display.init()
                pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            elif event.key == pygame.K_ESCAPE:
                pygame.display.init()
                pygame.display.set_mode(dimensions)

        if pygame.mouse.get_pressed()[0] == 1:  # mouse.get_pressed() returns the 0 1 tuple of (left,mid,right) click
            ship1.shoot()

    keys = pygame.key.get_pressed()
    up, down, right, left = keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_RIGHT], keys[pygame.K_LEFT]
    all_sprites.update(up,down,right,left)
    all_sprites.draw(window)
    scoreBoard = font.render("Score: {}".format(score),1,(250,250,250))
    window.blit(scoreBoard,(window.get_size()[0]-scoreBoard.get_size()[0],window.get_size()[1]-scoreBoard.get_size()[1]))

    status = pygame.sprite.spritecollide(ship1,rndmpieces,True,collided=pygame.sprite.collide_circle) # True value for killing rndmpieces itself,returns rndmpiece

    hits = pygame.sprite.groupcollide(bullets,rndmpieces,True,True)  #checks if two group has relations in common

    if hits:
        exploseMeteor = pygame.mixer.Sound(random.choice(explosions))
        exploseMeteor.set_volume(0.3)
        exploseMeteor.play()
        score += 1
        for all_meteors in hits.values():
            for theMeteor in all_meteors:
                crashes = Crash(theMeteor,crash)
                all_sprites.add(crashes)
    if status:

        if ship1.shield > ship1.shield * (10/100):
            crashS = pygame.mixer.Sound(hitSound[0]).play()

        for aMeteor in status:
            ship1.shield -= aMeteor.radius*3
            crash_ship = Crash(aMeteor, ship_crash)
            all_sprites.add(crash_ship)
            if ship1.shield <= 0:
                ship1.ship_health -= 1
                ship1.hide()
                if ship1.ship_health == 0:
                    pygame.mixer.Sound(hitSound[1]).play()
                    pygame.time.wait(2500)
                    if game_over:
                        gameOver()
                        level = 0
                        for anyMeteor in status:
                            anyMeteor.kill()
                ship1.shield = 100
                if ship1.ship_health == 0:
                    ship1.ship_health = 3
    if len(rndmpieces) == 0:
        if waitingTime:
            endTime = pygame.time.get_ticks()
            waitingTime = False
            levelFont = pygame.font.SysFont("arial",60,True,False)
            writingLevel = levelFont.render("Level {}".format(level+1),1,(250,250,250))
        window.blit(writingLevel, ((width / 2).__int__(), (height / 2).__int__()))
        if pygame.time.get_ticks() - endTime > 4000:
            waitingTime=True
            level += 1
            for i in range(15*level):
                rndmpiece = RandomPieces()
                all_sprites.add(rndmpiece)
                rndmpieces.add(rndmpiece)

    pygame.display.update()

