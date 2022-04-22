#!/usr/bin/env python3

# *****************************************************************
# A Python pygame that allows user to play the game breakout.

# @author Steve Meadows
# @version Winter 2022
# ***************************************************************** 

import pygame as pg
import random

#*****************************************************************
    # Constructor creates an overlay instance to display text on 
    # game screen.
    # @param pygame.sprite.Sprite - a visual game object
#   *****************************************************************/
class Overlay(pg.sprite.Sprite):

    # starting score of game 
    score = 0

    # starting lives of user 
    lives = 5

    # initialize Overlay and set fonts and texts
    def __init__(self):
        super().__init__()
        self.font = pg.font.Font('freesansbold.ttf',16) 
        self.image = pg.Surface((200, 30))
        self.image = self.font.render('Score: ' + str(self.score) 
        + '  Lives: ' + str(self.lives), True, (0,0,0), None)
        self.rect = self.image.get_rect() 

    # static method to retrive score 
    @staticmethod
    def get_score():
        return Overlay.score

    # static method to set score 
    @staticmethod
    def set_score():
        Overlay.score = Overlay.score + 1

    # static method to set lives 
    @staticmethod
    def set_lives():
        Overlay.lives = Overlay.lives - 1

    # static method to retrive lives 
    @staticmethod
    def get_lives():
        return Overlay.lives

    # update method that constantly updates what's written on the screen
    # it receives a @param: game, which lets the overlay class know if the
    # game is over. If it is, it makes sure to display lives as 0.
    def update(self, game): 
        if game is False:
            self.image = self.font.render('Score: ' + str(Overlay.score) 
            + '  Lives: ' + str(Overlay.lives), True, (0,0,0), None)
        else:
            self.image = self.font.render('Score: ' + str(Overlay.score) 
            + '  Lives: 0', True, (0,0,0), None)

#*****************************************************************
    # Constructor creates an block instance to display text on 
    # game screen.
    # @param pygame.sprite.Sprite - a visual game object
    # @param x - x coordinate to place the block
    # @param y - y coordinate to place the block
#   *****************************************************************/
class Block(pg.sprite.Sprite ):

    # Initializes block
    def __init__(self, x, y):
        r = random.randint
        super().__init__()
        self.width = 80
        self.height = 40
        self.image = pg.Surface((80, 40))
        self.color = ( r(0,255), r(0,255), r(0,255) )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 766
        self.balls = None

    # Update method for block
    def update(self):

        # collide variable
        hit = pg.sprite.spritecollide(self, Block.balls, False)

        # if the block is hit by a ball, then the block's health decreases
        if hit:
            self.health = self.health - 500
            # self.color = self.color + (-25,-25,-25)

        # if the block's health is or is below zero, then the block is
        # destroyed
        if self.health <= 0: 
            self.kill()
            
    def setBalls(self, balls):
        self.balls = balls
    
#*****************************************************************
    # Ball constructor class.
    # @param pygame.sprite.Sprite - a visual game object
#   *****************************************************************/
class Ball(pg.sprite.Sprite):

    # boolean to tell the ball if the game is over or not
    game_over = False

    # initializes mixer to play sound
    pg.mixer.init()

    # sound played when block is hit
    BLOCK_BEEP = pg.mixer.Sound("block__beep.wav") 

    # sound played when paddle is hit
    PADDLE_BEEP = pg.mixer.Sound("paddle_beep.wav")

    # sound played when you lose a life
    MINUS_LIFE = pg.mixer.Sound("death.wav")
    
    # initializes a new ball
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.image.fill( (255,255,255) )
        pg.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
        self.rect.x = 368
        self.rect.y = 300
        self.velocity = [6,6]
        self.paddles = None
        self.blocks = None
        
    # method called to resurrect balls when a life is lost
    def new_life(self):

        # if there are lives left it draws a new ball
        if Overlay.get_lives() > 1:
            Overlay.set_lives()
            pg.time.delay(2000)
            pg.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
            self.rect.x = 200
            self.rect.y = 300
            self.rect.x += self.velocity[0]
            self.rect.y -= self.velocity[1]

        # if not it stops the ball from moving and tells the ball
        # class there are no more lives left
        else:
            self.rect.x += 0
            self.rect.y += 0
            Ball.game_over = True
            
    # static method that retreives game status from the ball
    @staticmethod        
    def game_done():
        return Ball.game_over

    # update method for ball class
    def update(self):

        # moves ball perpetually
        self.rect.x += self.velocity[0]
        self.rect.y -= self.velocity[1]

        # bounce for left side of screen
        if self.rect.x < 0:
            self.rect.x = 0
            self.velocity[0] = -self.velocity[0]
        
        # bounce for right side of screen
        if self.rect.x > 790:
            self.rect.x = 790
            self.velocity[0] = -self.velocity[0]

        # bounce for top of screen
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity[1] = -self.velocity[1]

        # drops a life and calls for a new ball if lives are left
        # if ball hits the bottom of screen
        if self.rect.y > 600:
            if Ball.game_over is False:
                self.MINUS_LIFE.play()

            #new_life() method call
            self.new_life()
            

        # collide variable for paddle
        collisions = pg.sprite.spritecollide(self, Ball.paddles, False)

        # collide variable for blocks
        smashes = pg.sprite.spritecollide(self, Ball.blocks, False)
        
        # tells the ball what to do if it collides with a paddle
        if collisions:
            self.PADDLE_BEEP.play()
            self.velocity[1] = -self.velocity[1]

        # tells the ball what to do if it collides with a block
        if smashes:
            self.BLOCK_BEEP.play()
            self.velocity[0] = self.velocity[0]
            self.velocity[1] = -self.velocity[1] 
            Overlay.set_score() 

    def setPaddles(self, paddles):
        self.paddles = paddles

    def setBlocks(self, blocks):
        self.blocks = blocks

#*****************************************************************
    # Constructor creates an paddle instance to control the balls
    # direction
    # @param pygame.sprite.Sprite - a visual game object
#   *****************************************************************/
class Paddle(pg.sprite.Sprite):

    # instantiates a new paddle
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((200,10))
        self.image.fill( (0,0,0) )
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 575
        self.velocity = [15, 0]
        
    #update method for paddle
    def update(self):

        # tells paddle what to do to move left and when
        # it hits the left wall
        key_input = pg.key.get_pressed()
        if key_input[pg.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocity[0]

        # tells paddle what to do to move right and when
        # it hits the right wall
        if key_input[pg.K_RIGHT]and self.rect.x < 600:
            self.rect.x += self.velocity[0]

        # nothing is pressed, don't move the paddle
        else:
            self.rect.x += self.velocity[1]

#*****************************************************************
    # New game constructor
#   *****************************************************************/
class Game:
    def __init__(self):
        pg.init()
        self.__running = False
        pg.display.set_caption("Breakout")

        #where we are drawing to: Width x Height
        self.screen = pg.display.set_mode( (800, 600) )

        MUSIC = pg.mixer.Sound("music.mp3") 
        channel1 = pg.mixer.find_channel()
        channel1.play(MUSIC)

        self.clock = pg.time.Clock()
        self.blocks = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.paddles = pg.sprite.Group()
        self.overlays = pg.sprite.Group()

    # adds new blocks
    def addBlocks(self):
        x = 0
        y = -40
        rows = 5
        columns = 10

        for _ in range(rows):
            y = y + 40
            x= 0
            for _ in range(columns):
                self.blocks.add( Block(x,y) )
                x= x + 80

    # game loop
    def run(self):
        while self.__running:
            # Take events

            background = pg.image.load("background.png")
            pg.mixer.pre_init()
            pg.mixer.init()
            GAME_OVER = pg.mixer.Sound("game_over.wav")  
                    
            events = pg.event.get()
            self.game_over = False

            for event in events:
                if event.type == pg.QUIT:
                    self.__running = False
                    pg.quit()
                    exit()
            
            for event in events: 
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    while True: #Infinite loop that will be broken when the user press the space bar again
                        event = pg.event.wait()
                        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                            break #Exit infinite loop

            for event in events:
                if event.type == pg.KEYDOWN and event.key == pg.K_n:
                    self.addBalls( Ball())

            # Update updateable objects
            self.overlays.update(self.game_over)
            self.paddles.update()
            self.balls.update()
            self.blocks.update()
            # self.__running = True

            # Redraw
            self.screen.blit(background, (0, 0)) 
            self.blocks.draw(self.screen)
            self.paddles.draw(self.screen)
            self.balls.draw(self.screen)
            self.overlays.draw(self.screen)
            
            self.game_over = Ball.game_done()
            
            if self.game_over is True:
                self.removeBalls()
                font = pg.font.Font(None, 70)
                game_over_text = font.render("GAME OVER", True, (0, 0,0))
                self.screen.blit(game_over_text, (250,225))
                GAME_OVER.play()
                self.setRunning(False)

            pg.display.flip()
            self.clock.tick(60)

    def setRunning(self, running):
        self.__running = running

    def addPaddle(self, paddle):
        self.paddles.add(paddle)

    def addBalls(self, ball):
        self.balls.add(ball)
    
    def addOverlays(self, overlays):
        self.overlays.add(overlays)

    # def addBlocks(self, block):
    #     self.blocks.add(block)

    def getPaddles(self):
        return self.paddles

    def getBlocks(self):
        return self.blocks

    def getBalls(self):
        return self.balls

    def removeBalls(self):
        return self.balls.remove(self, Ball())
    
#*****************************************************************
    # Constructor creates a die of specified size X size pixels
    # @param size the length of each side in pixels
#    *****************************************************************/
def main():
    game = Game()
    game.addOverlays( Overlay() )
    game.addBlocks()
    game.addPaddle( Paddle() )
    Ball.paddles = game.getPaddles()
    Ball.blocks = game.getBlocks()  
    Block.balls = game.getBalls()
    game.addBalls( Ball() )
    game.setRunning(True)
    game.run()
    

if __name__ == '__main__':
    main()