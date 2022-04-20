#!/usr/bin/env python3

#!/usr/bin/env python3

import pygame as pg
import random

class Overlay(pg.sprite.Sprite):

    score = 0
    lives = 5

    def __init__(self):
        super().__init__()
        self.font = pg.font.Font('freesansbold.ttf',16) 
        self.image = pg.Surface((200, 30))
        self.image = self.font.render('Score: ' + str(self.score) + '  Lives: ' + str(self.lives), True, (0,0,0), None)
        self.rect = self.image.get_rect() 

    @staticmethod
    def get_score():
        return Overlay.score

    @staticmethod
    def set_score():
        Overlay.score = Overlay.score + 1

    @staticmethod
    def set_lives():
        Overlay.lives = Overlay.lives - 1

    @staticmethod
    def get_lives():
        return Overlay.lives

    def update(self, game): 
        if game is False:
            self.image = self.font.render('Score: ' + str(Overlay.score) + '  Lives: ' + str(Overlay.lives), True, (0,0,0), None)
        else:
            self.image = self.font.render('Score: ' + str(Overlay.score) + '  Lives: 0', True, (0,0,0), None)

class Block(pg.sprite.Sprite ):
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

    def update(self):
        hit = pg.sprite.spritecollide(self, Block.balls, False)

        if hit:
            self.health = self.health - 500
            # print(self.health)

        if self.health <= 0: 
            self.kill()
            
    
    def setBalls(self, balls):
        self.balls = balls
    
class Ball(pg.sprite.Sprite):

    game_over = False
    pg.mixer.init()
    BLOCK_BEEP = pg.mixer.Sound("block__beep.wav") 
    PADDLE_BEEP = pg.mixer.Sound("paddle_beep.wav")
    MINUS_LIFE = pg.mixer.Sound("death.wav")
    
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

    # @staticmethod
    # def get_ball_status():
    #     return Ball.ball_killed

    # @staticmethod
    # def set_ball_status():
    #     Ball.ball_killed = True

    def new_life(self):
        if Overlay.get_lives() > 1:
            Overlay.set_lives()
            pg.time.delay(2000)
            # self.kill = False
            pg.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
            self.rect.x = 200
            self.rect.y = 300
            self.rect.x += self.velocity[0]
            self.rect.y -= self.velocity[1]

        else:
            self.rect.x += 0
            self.rect.y += 0
            Overlay.set_lives()
            Ball.game_over = True
            
    @staticmethod        
    def game_done():
        return Ball.game_over


    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y -= self.velocity[1]
        if self.rect.x < 0:
            self.rect.x = 0
            self.velocity[0] = -self.velocity[0]
        if self.rect.x > 790:
            self.rect.x = 790
            self.velocity[0] = -self.velocity[0]
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity[1] = -self.velocity[1]
        if self.rect.y > 600:
            if Ball.game_over is False:
                channel = pg.mixer.find_channel()
                channel.play(self.MINUS_LIFE)
            # 
            self.new_life()
            

        
        collisions = pg.sprite.spritecollide(self, Ball.paddles, False)
        smashes = pg.sprite.spritecollide(self, Ball.blocks, False)
        
        if collisions:
            channel = pg.mixer.find_channel()
            channel.play(self.PADDLE_BEEP)
            self.velocity[1] = -self.velocity[1]

        if smashes:
            channel = pg.mixer.find_channel()
            channel.play(self.BLOCK_BEEP)
            self.velocity[0] = self.velocity[0]
            self.velocity[1] = -self.velocity[1] 
            Overlay.set_score() 

    def setPaddles(self, paddles):
        self.paddles = paddles

    def setBlocks(self, blocks):
        self.blocks = blocks
    
class Paddle(pg.sprite.Sprite):
    # explodifiers = None
    def __init__(self):
        super().__init__()

        #something we can draw on
        self.image = pg.Surface((200,10))

        #color of the object
        self.image.fill( (0,0,0) )

        self.rect = self.image.get_rect()

        self.rect.x = 200
        self.rect.y = 575

        # pg.draw.rect(self.image, (255,0,0), (200, 575, 200, 575))        
        self.velocity = [15, 0]
        

    def update(self):

        key_input = pg.key.get_pressed()
        if key_input[pg.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocity[0]

        if key_input[pg.K_RIGHT]and self.rect.x < 600:
            self.rect.x += self.velocity[0]

        else:
            self.rect.x += self.velocity[1]

    # def setExplodifiers(self, explodifiers):
    #     self.explodifiers = explodifiers

class Game:
    def __init__(self):
        pg.init()
        self.__running = False
        pg.display.set_caption("PyGame")

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

            self.__running = True

            # Redraw
            self.screen.blit(background, (0, 0)) 
            self.blocks.draw(self.screen)
            self.paddles.draw(self.screen)
            self.balls.draw(self.screen)
            self.overlays.draw(self.screen)
            
            self.game_over = Ball.game_done()
            
            if self.game_over is True:
                self.overlays.update(self.game_over)
                font = pg.font.Font(None, 70)
                game_over_text = font.render("GAME OVER", True, (0, 0,0))
                self.screen.blit(game_over_text, (250,225))
                channel = pg.mixer.find_channel()
                channel.play(GAME_OVER)

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
    
    # def getOverlays(self):
    #     return self.overlays

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
    game.setRunning(False)

if __name__ == '__main__':
    main()