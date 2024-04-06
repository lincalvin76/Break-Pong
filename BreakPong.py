#libraries
import pygame
import random
import pygame.freetype

#Controls
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#Sounds
#All sound was taken from pixaby

#initialize mixer
pygame.mixer.init()

#play background music
pygame.mixer.music.set_volume(0.3) #volume
pygame.mixer.music.load("gameMusicLoop.mp3") #music
pygame.mixer.music.play(loops=-1) #inf loop

#setup sounds
brickHit = pygame.mixer.Sound("brickHit.mp3")
ballBounce = pygame.mixer.Sound("ballBounce.mp3")
pointScore = pygame.mixer.Sound("pointScore.mp3")

# change the volume for all sounds
brickHit.set_volume(0.3)
ballBounce.set_volume(0.5)
pointScore.set_volume(0.5)


#Size
width = 1280
height = 500

x = 0
y = 1.03

#Scoreboard
score1 = 0 #Initialize the score for P1
score2 = 0 #Initialize the score for P2

#Classes

#P1
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.surf = pygame.Surface((10, 70)) #Rect Size
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(
            center=(
                width/4, height/2 #Rect Location
            )
        )

    #Movement
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
    #Borders
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= height:
            self.rect.bottom = height

#P2
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surf = pygame.Surface((10, 70)) #Rect Size 10,70
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(
            center=(
                (3*width)/4, height/2 #Rect Location
            )
        )

    #Movement
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
    #Borders
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= height:
            self.rect.bottom = height

#Ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((7,7)) #Ball Size
        self.surf.fill((255,255,255)) #Ball Color
        self.rect = self.surf.get_rect(
            center=(
                (width/2,height/2)
            )
        )
        #These variables down here are for changing up the initial direction for more varied gameplay.
        rng1=random.randrange(0,2) #RNG for the initial X direction.
        rng2=random.randrange(0,2) #RNG for the initial Y direction.
        if rng1 == 1:
            Xinit=-1
        if rng1 == 0:
            Xinit=1
        if rng2 == 1:
            Yinit=-1
        if rng2 == 0:
            Yinit=1

        self.speed = random.randrange(2,6)*Xinit #Ball X Speed with variation
        self.reflect = random.randrange(2,6)*Yinit #Ball Y Speed with variation

    #There may be a slight bug where the ball disappears near the paddle when hitting the roof when I used a random number, couldn't figure it out.    
    def update(self): 
        #Globalize the scores so they can be used in here
        global score1
        global score2

        self.rect.move_ip(self.speed, self.reflect)#Move the ball using x and y
        if self.rect.right < 0: #If ball gets off screen to the right reset.
            self.__init__()
            score1 +=1 #add point
            pointScore.play() #play sound
        if self.rect.left > width: #If ball gets off screen to the left reset.
            self.__init__()
            score2 +=1 #add point
            pointScore.play() #play sound
        if self.rect.top < 0: #If ball hits the top, change the y value to the opposite sign
            self.reflect = -self.reflect
            if self.speed < 0: #increase speed
                self.speed -= 0.2
            else:
                self.speed += 0.2
            ballBounce.play()
        elif self.rect.bottom > height: #If ball hits the bottom, change the y value to the opposite sign
            self.reflect = -self.reflect
            if self.speed < 0: #increase speed
                self.speed -= 0.2
            else:
                self.speed += 0.2
            ballBounce.play()
        
        if self.rect.colliderect(player1): #If ball hits player1, change the x value
            self.speed = -self.speed #increase speed
            if self.speed < 0:
                self.speed -= 0.2
            else:
                self.speed += 0.2
            ballBounce.play()
        elif self.rect.colliderect(player2): #If ball hits player2, change the x value
            self.speed = -self.speed
            if self.speed < 0: #increase speed
                self.speed -= 0.2
            else:
                self.speed += 0.2
            ballBounce.play()

        for i in blocks: #check every single block
            if self.rect.colliderect(i): #if ball collides with block
                self.speed = -self.speed #reverse speed
                if self.speed < 0: #increase speed
                    self.speed -= 0.2
                else:
                    self.speed += 0.2

#Bricks
class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.surf = pygame.Surface((10,20)) #size
        self.surf.fill((255,255,255)) #Color
        self.rect = self.surf.get_rect(center = (((width/6)- x), ((height/1.03) - y))) #Positioning
        #print(self.rect.center) <- Used for checking position

    
    def update(self):
        for i in balls: #check the singular ball
            if self.rect.colliderect(i): #if any blocks collide with the ball
                self.kill() #delete the block
                brickHit.play() #play brick hitting sound

#Line
class Line(pygame.sprite.Sprite):
    def __init__(self):
        super(Line, self).__init__()
        self.surf = pygame.Surface((5,height))
        self.surf.fill((255,255,255))
        self.surf.set_alpha(100)
        self.rect = self.surf.get_rect(center = (width/2, height/2))



#Start Game

pygame.init() #Initialize game
clock = pygame.time.Clock() #The Clock
screen = pygame.display.set_mode((width,height)) #Make Screen

player1 = Player1() #Create player1
player2 = Player2() #Create player2
ball = Ball() #Create Ball
line = Line()

all_sprites = pygame.sprite.Group() #Create a group for the sprites
balls = pygame.sprite.Group() #Group the balls when creating them
blocks = pygame.sprite.Group()
all_sprites.add(line)
all_sprites.add(player1) #Make player1 Visible
all_sprites.add(player2) #Make player2 Visible


ADDBALL = pygame.USEREVENT +1 #AddBall Event
add_ball = pygame.event.Event(ADDBALL) #Assigning it as an event

running = True 
pygame.event.post(add_ball) #Add a event at the end of the list for the ball

#BRICK SPAWNS
#For the numbers between each loop, i just got them by testing over and over again.

#Left Row 1
for i in range(20): #20 bricks
        new_block = Block() #create brick
        blocks.add(new_block) #add to group
        x = 0 #set width as is so width/6
        y += 25 #increase the height each time

y = -25 #tested

#Left Row 2
for i in range(23): #23 bricks (slight variation)
        new_block = Block() #create brick
        blocks.add(new_block) #add to group
        x = 15 #move to the left 15 units
        y += 23 #move up by 23 to reach the top

y = 1.03 #set y back to the bottom
x = -854 #set up x position for the right side

#Right Row 1
for i in range(20): #20 bricks
        new_block = Block() #create brick
        blocks.add(new_block) #add to group
        x = -854 #keep this right side x
        y += 25 #increase the height each time

x = -869 #move it right 15 units
y = -25 #same as before

#Right Row 2
for i in range(23): #23 bricks (slight variation)
        new_block = Block() #create brick
        blocks.add(new_block) #add to group
        x = -869 #keep it in the right position
        y += 23 #move up by 23 to reach the top

all_sprites.add(blocks) #make visible

r = random.randrange(100,200) #random red
g = random.randrange(100,200) #random green
b = random.randrange(100,200) #random blue

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN: 
            if event.key == K_ESCAPE: #ESC = Exit
                running = False
        elif event.type == QUIT: #X Key = Exit
            running = False
        elif event.type == ADDBALL: #Adding ball event
            new_ball = Ball()
            balls.add(new_ball)
            all_sprites.add(new_ball)
                

    pressed_keys = pygame.key.get_pressed()
    player1.update(pressed_keys) #Player 1 Keys (W and S)
    player2.update(pressed_keys) #Player2 Keys (Up and Down Arrow)
    balls.update() #Update ball to move
    blocks.update() #Update any blocks that are deleting

    screen.fill((r,g,b)) #Make the background a random bright color
    font = pygame.font.SysFont("comicsansms", 15) #Setting a font
    font.bold = True
    scoreboard1 = font.render("P1: "+str(score1), 1, (255,255,255)) #Displaying score for P1
    scoreboard2 = font.render("P2: "+str(score2), 1, (255,255,255)) #Displaying score for P2
    screen.blit(scoreboard1, (((width/2)-200), 10)) # scoreboard 1 position
    screen.blit(scoreboard2, (((width/2)+200), 10)) # scoreboard 2 position

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect) #Make every single sprite visible
    
    pygame.display.flip()
    clock.tick(60) #FPS
