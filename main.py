import pygame
from pygame.locals import *
import time
import random

class Cake:
    def __init__(self,parent_screen):
        self.parent_screen=parent_screen
        self.image= pygame.image.load("resources/cake.jpg").convert()
        self.x=40*3
        self.y=40*3

    
    def draw(self):
        
         self.parent_screen.blit(self.image, (self.x, self.y))
         pygame.display.flip()


    def move(self):
        self.x = random.randint(1,20)*40
        self.y = random.randint(1,15)*40   

class Snake:
    def __init__(self, surface,length):
        self.parent_screen = surface
        self.block = pygame.image.load("resources/snake.jpg").convert()
        self.length=length
        self.x = [40]*length
        self.y = [40]*length
        
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1,0,-1):
          self.x[i]=self.x[i-1]
          self.y[i]=self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= 40
        if self.direction == 'right':
            self.x[0] += 40
        if self.direction == 'up':
            self.y[0] -= 40
        if self.direction == 'down':
            self.y[0] += 40

        self.draw() 


    def draw(self):
        self.parent_screen.fill((241, 196, 203))
        
        for i in range (self.length):
         self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
    
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("CAUSE MY BRANCH IS ELECTRICAL!!")
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.cake=Cake(self.surface)
        self.clock = pygame.time.Clock()  
        self.speed = 0.5

    def reset(self):
        self.snake = Snake(self.surface)
        self.cake = Cake(self.surface)
        self.speed = 0.5



    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + 40:
            if y1 >= y2 and y1 < y2 + 40:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.cake.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.cake.x, self.cake.y):
                
                self.snake.increase_length()
                self.cake.move()
                self.speed *= 0.75  
                self.clock.tick(60) 

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                
                raise "smasshh"

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            
            raise "Hit "

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"GRADE: {self.snake.length}",True,(0,0,0))
        self.surface.blit(score,(850,10))

    def show_game_over(self):
    #  self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"   YOU ARE FINISHED! Your GRADE:{self.snake.length}", True, (0, 0, 0))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(" ENTER TO TAKE A REBIRTH. ESCAPE TO SEEK HEAVEN!", True, (0, 0, 0))
        self.surface.blit(line2, (150, 350))
        
        pygame.display.flip()



    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
              
                pygame.time.delay(5000)
                self.reset()

            time.sleep(self.speed)


if __name__ == '__main__':
    game = Game()
    game.run()