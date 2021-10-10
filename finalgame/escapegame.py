import pygame, sys, time
from pygame.locals import *

PLAYERMOVE = 2.5

#set up pygame.
pygame.init() #initialize all imported pygame modules

#set up the window.
SCR_WID, SCR_HEI = 800, 800 #constants
screen = pygame.display.set_mode((SCR_WID, SCR_HEI)) #screen size
pygame.display.set_caption('House Escape') #set current window caption

def PressKey():
    while True:
        for event in pygame.event.get(): #get events from the queue
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR) #create surface object
    textrect = textobj.get_rect() #get rectangular area of the surface
    textrect.topleft = (x, y) #select coordinates from left most point
    surface.blit(textobj, textrect) #draw to screen

#font
font = pygame.font.SysFont(None, 48) #create font object from the system fonts to create a surface object

#start screen
BACKGROUNDCOLOR = (0, 0, 0) #black
TEXTCOLOR = (255, 255, 255) #white
screen.fill(BACKGROUNDCOLOR) #fill screen with black
drawText('House Escape', font, screen, (SCR_WID / 3), (SCR_HEI / 3))
drawText('Press a key to start.', font, screen, (SCR_WID / 3) - 30, (SCR_HEI / 3) + 50)
drawText('Choose the right key to escape the closet.', font, screen, (60), (400))
drawText('Choose the right tool to leave the bedroom.', font, screen, (50), (500))
drawText('Collect four more specific objects to escape', font, screen, (42), (600))
drawText('the house', font, screen, (300), (650))
pygame.display.update() #update screen
PressKey()

#background
bg = pygame.image.load('gamemap.png') #load new image from file

#sound
itempickup = pygame.mixer.Sound('itempickup.wav') #create a new Sound object from a file
pygame.mixer.music.load('spooky.mid') #load a music file for playback

#closet
keyImage1 = pygame.image.load('key1.png')
keyImage1Rect = keyImage1.get_rect()
keyImage1Rect.center = 640, 770

keyImage2 = pygame.image.load('key2.png')
keyImage2Rect = keyImage2.get_rect()
keyImage2Rect.center = 770, 700

#bedroom
axeImage = pygame.image.load('axe.png')
axeImageRect = axeImage.get_rect()
axeImageRect.center = 470, 515

mallotImage = pygame.image.load('mallot.png')
mallotImageRect = mallotImage.get_rect()
mallotImageRect.center = 770, 400

#house search
grenadeImage = pygame.image.load('grenade.png')
grenadeImageRect = grenadeImage.get_rect()
grenadeImageRect.center = 100, 520

keyImage3 = pygame.image.load('key3.png')
keyImage3Rect = keyImage3.get_rect()
keyImage3Rect.center = 70, 680

wrenchImage = pygame.image.load('wrench.png')
wrenchImageRect = wrenchImage.get_rect()
wrenchImageRect.center = 210, 110

knifeImage = pygame.image.load('knife.png')
knifeImageRect = knifeImage.get_rect()
knifeImageRect.center = 768, 250

pistolImage = pygame.image.load('pistol.png')
pistolImageRect = pistolImage.get_rect()
pistolImageRect.center = 100, 380

shotgunImage = pygame.image.load('shotgun.png')
shotgunImageRect = shotgunImage.get_rect()
shotgunImageRect.center = 400, 15

shovelImage = pygame.image.load('shovel.png')
shovelImageRect = shovelImage.get_rect()
shovelImageRect.center = 210, 775

inventory = []
def addtoinventory(item):
    inventory.append(item) #add item to inventory

def closetkey(playerRect, keyImage1Rect):
    if playerRect.colliderect(keyImage1Rect): #test if rectangles overlap
        addtoinventory('gold key')
        itempickup.play() #play music file
        print("Your inventory: ", inventory)

def bedroommallot(playerRect, mallotImageRect):
    if playerRect.colliderect(mallotImageRect):
        addtoinventory('mallot')
        itempickup.play()
        print("Your inventory: ", inventory)
        
def kitchenknife(playerRect, knifeImageRect):
    if 'knife' not in inventory:
        screen.blit(knifeImage, knifeImageRect)
        if playerRect.colliderect(knifeImageRect):
            addtoinventory('knife')
            itempickup.play()
            print("Your inventory: ", inventory)

def livingwrench(playerRect, wrenchImageRect):
    if 'wrench' not in inventory:
        screen.blit(wrenchImage, wrenchImageRect)
        if playerRect.colliderect(wrenchImageRect):
            addtoinventory('wrench')
            itempickup.play()
            print("Your inventory: ", inventory)

def bathpistol(playerRect, pistolImageRect):
    if 'pistol' not in inventory:
        screen.blit(pistolImage, pistolImageRect)
        if playerRect.colliderect(pistolImageRect):
            addtoinventory('pistol')
            itempickup.play()
            print ("Your inventory: ", inventory)

def bloodkey(playerRect, keyImage3Rect):
    if 'bronze key' not in inventory:
        screen.blit(keyImage3, keyImage3Rect)
        if playerRect.colliderect(keyImage3Rect):
            addtoinventory('bronze key')
            itempickup.play()
            print("Your inventory: ", inventory)
            
starttime = time.time() #time functions returns num of secs passed since epoch(point where time begins)
timeallowed = 40 #seconds

#player class
class Player(pygame.sprite.Sprite): #base class for visible game objects.
    
    def __init__(self, dx, dy, file):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(file).convert_alpha() #gets rid of black box behind player (transparency)
        self.rect = self.image.get_rect(x = dx, y = dy) #get rectangular area of the surface

        self.moveLeft = self.moveRight = self.moveUp = self.moveDown = False

    def update(self, inventory):
        if len(inventory) == 0:
            closetkey(self.rect, keyImage1Rect)
            SCR_WIDCLOSET, SCR_HEICLOSET = 800, 690
            if self.moveLeft and self.rect.left > SCR_HEICLOSET - 90:
                self.rect.move_ip(-1 * PLAYERMOVE, 0) #moves rectangle in place
            if self.moveRight and self.rect.right < SCR_WIDCLOSET:
                self.rect.move_ip(PLAYERMOVE, 0)
            if self.moveUp and self.rect.top > SCR_HEICLOSET - 40:
                self.rect.move_ip(0, -1 * PLAYERMOVE)
            if self.moveDown and self.rect.bottom < SCR_HEICLOSET + 100:
                self.rect.move_ip(0, PLAYERMOVE)

        if len(inventory) == 1:
            bedroommallot(self.rect, mallotImageRect)
            SCR_WIDBEDROOM, SCR_HEIBEDROOM = 800, 400
            if self.moveLeft and self.rect.left > SCR_HEIBEDROOM + 13:
                self.rect.move_ip(-1 * PLAYERMOVE, 0)
            if self.moveRight and self.rect.right < SCR_WIDBEDROOM:
                self.rect.move_ip(PLAYERMOVE, 0)
            if self.moveUp and self.rect.top > SCR_HEIBEDROOM - 40:
                self.rect.move_ip(0, -1 * PLAYERMOVE)
            if self.moveDown and self.rect.bottom < SCR_HEIBEDROOM + 300:
                self.rect.move_ip(0, PLAYERMOVE)

        if len(inventory) >= 2:
            kitchenknife(self.rect, knifeImageRect)
            livingwrench(self.rect, wrenchImageRect)
            bathpistol(self.rect, pistolImageRect)
            bloodkey(self.rect, keyImage3Rect)
            SCR_WIDHOUSE, SCR_HEIHOUSE = 800, 800
            if self.moveLeft and self.rect.left > 0:
                self.rect.move_ip(-1 * PLAYERMOVE, 0)
            if self.moveRight and self.rect.right < SCR_WIDHOUSE:
                self.rect.move_ip(PLAYERMOVE, 0)
            if self.moveUp and self.rect.top > 0:
                self.rect.move_ip(0, -1 * PLAYERMOVE)
            if self.moveDown and self.rect.bottom < SCR_HEIHOUSE:
                self.rect.move_ip(0, PLAYERMOVE)

    def events(self, event):
        if event.type == KEYDOWN:
##            if event.key == K_z:
##                reverseCheat = True
##            if event.key == K_x:
##                slowCheat = True
            if event.key == K_LEFT or event.key == K_a:
                self.moveRight = False
                self.moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                self.moveLeft = False
                self.moveRight = True
            if event.key == K_UP or event.key == K_w:
                self.moveDown = False
                self.moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                self.moveUp = False
                self.moveDown = True
                        
        if event.type == KEYUP:
            if event.key == K_z:
                reverseCheat = False
            if event.key == K_x:
                slowCheat = False
            if event.key == K_ESCAPE:
                terminate()

            if event.key == K_LEFT or event.key == K_a:
                self.moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                self.moveRight = False
            if event.key == K_UP or event.key == K_w:
                self.moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                self.moveDown = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        
def main():
    while True:
        player = Player(680, 700, "littleguy.png")
        pygame.mixer.music.play(-1, 0.0) #start the playback of the music stream

        while True:
            #gameloop
            for event in pygame.event.get(): #get events from the queue
                if event.type == QUIT:
                    print("Game exited by user")
                    pygame.quit()
                    sys.exit()

                #if number of seconds passed is greater than the time allowed
                if time.time() > starttime + timeallowed: 
                    print("OH NO! Your kidnapper came back before you could escape. You lost the game.")
                    pygame.quit()
                    sys.exit

                player.events(event)
                        
            player.update(inventory)

            screen.fill((5,5,5))
            screen.blit(bg,(0,0))

            if 'knife' not in inventory:
                screen.blit(knifeImage, knifeImageRect)

            if 'gold key' not in inventory:
                screen.blit(keyImage1, keyImage1Rect)

            if 'mallot' not in inventory:
                screen.blit(mallotImage, mallotImageRect)

            if 'wrench' not in inventory:
                screen.blit(wrenchImage, wrenchImageRect)

            if 'pistol' not in inventory:
                screen.blit(pistolImage, pistolImageRect)

            if 'bronze key' not in inventory:
                screen.blit(keyImage3, keyImage3Rect)

            player.draw(screen)

            screen.blit(keyImage2, keyImage2Rect)
            screen.blit(axeImage, axeImageRect)
            screen.blit(knifeImage, knifeImageRect)
            screen.blit(grenadeImage, grenadeImageRect)
            screen.blit(shotgunImage, shotgunImageRect)
            screen.blit(shovelImage, shovelImageRect)

            if len(inventory) == 6:
                print("You escaped in time!")
                pygame.quit()
                sys.exit()

            #pygame.display.flip()
            pygame.display.update() #update screen
            
main()
