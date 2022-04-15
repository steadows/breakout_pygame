#!/usr/bin/env python3

#!/usr/bin/env python3

import pygame as pg
import random




    
        # self.image = pg.Surface((200,50))

    # def setScore(self, score_val):
    #     self.score = self.score + score_val

    # def update(self):
    #     pg.font.Font.render("Score :" + str(self.score), True, (0,0,0))

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
            print(self.health)

        if self.health <= 0: 
            self.kill()
    
    def setBalls(self, balls):
        self.balls = balls
    
class Ball(pg.sprite.Sprite):
    
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
        if self.rect.y > 590:
            self.rect.y = 590
            self.velocity[1] = -self.velocity[1]

        

        collisions = pg.sprite.spritecollide(self, Ball.paddles, False)
        smashes = pg.sprite.spritecollide(self, Ball.blocks, False)
        
        if collisions:
            self.velocity[1] = -self.velocity[1]

        if smashes:
            self.velocity[0] = self.velocity[0]
            self.velocity[1] = -self.velocity[1]
            # Block.set_health(self,minus)
                  


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

        self.clock = pg.time.Clock()
        self.blocks = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.paddles = pg.sprite.Group()

        

    def showScore(self):
        score_val = 0
        lives = 5

        font = pg.font.Font('freesansbold.ttf',16) 
        textX = 10
        testY = 10
        score = font.render("Score: " + str(score_val) + " Lives: " + str(lives), True, (0,0,0))
        self.screen.blit(score, (textX,testY))

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
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    self.__running = False
                    pg.quit()
                    exit()
            
            

            # Update updateable objects
            self.paddles.update()
            self.balls.update()
            self.blocks.update()

            # Redraw
            self.screen.fill( (255, 255, 255) )
            
            self.blocks.draw(self.screen)
            self.paddles.draw(self.screen)
            self.balls.draw(self.screen)
            self.showScore()
            pg.display.flip()
            self.clock.tick(60)


    def setRunning(self, running):
        self.__running = running

    def addPaddle(self, paddle):
        self.paddles.add(paddle)

    def addBalls(self, ball):
        self.balls.add(ball)

    # def addBlocks(self, block):
    #     self.blocks.add(block)

    def getPaddles(self):
        return self.paddles

    def getBlocks(self):
        return self.blocks

    def getBalls(self):
        return self.balls

def main():
    game = Game()
    # game.addOverlay()
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