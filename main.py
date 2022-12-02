import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
X_SCREEN = 1000
Y_SCREEN = 600

# apple and its functions
class Apple:
    def __init__( self , parent_screen ):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/img/apple.jpg").convert()

        self.x = 120
        self.y = 120

    # drawing the apple to the board
    def draw( self ):
        self.parent_screen.blit( self.image, ( self.x, self.y ) )
        pygame.display.flip()

    # move the apple when it's eaten to a 
    # random position or when the game starts
    def move( self ):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 14) * SIZE

# create a snake and its attributes
class Snake:
    def __init__( self, parent_screen ):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/img/snake_body.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left( self ):
        self.direction = 'left'

    def move_right( self ):
        self.direction = 'right'

    def move_up( self ):
        self.direction = 'up'

    def move_down( self ):
        self.direction = 'down'

    def walk( self ):
        # update body
        for i in range(self.length - 1 , 0 , -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw( self ):
        for i in range( self.length ):
            self.parent_screen.blit( self.image, (self.x[i], self.y[i]) )

        pygame.display.flip()

    def increase_length( self ):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")

        pygame.mixer.init()
        # play background music when open the game
        self.play_background_music()
        
        # create a surface for the game
        self.surface = pygame.display.set_mode((X_SCREEN, Y_SCREEN))
        
        # create a snake and draw it on the screen
        self.snake = Snake(self.surface)

        self.snake.draw()

        # create an apple and draw it on the screen
        self.apple = Apple(self.surface)

        self.apple.draw()

    # play the background music fun
    def play_background_music(self):
        pygame.mixer.music.load('resources/msc/bg_music.mp3')
        pygame.mixer.music.play(-1, 0)

    # play music according to an event
    # snake bites itself/touches the wall OR
    # snake eats an apple
    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/msc/crash.mp3")

        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/msc/ding.mp3")

        pygame.mixer.Sound.play(sound)
        # pygame.mixer.music.stop()

    # will be called when you died and want
    # to play again so we'll need to reset
    # the snake body to 1 and the score to 0
    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    # find out if the head of the snake
    # collided with any other part of the body
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:

            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    # displaying the background/grass
    def render_background(self):
        bg = pygame.image.load("resources/img/background.jpg")
        self.surface.blit(bg, (0,0))

    # when you start playing the game this will be called
    def play(self):
        self.render_background()

        self.snake.walk()
        self.apple.draw()

        self.display_score()
        pygame.display.flip()

        # snake eating apple
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

        # snake colliding with the boundries of the window
        if not ( (0 <= self.snake.x[0] <= 1000 ) and (0 <= self.snake.y[0] <= 800)):
            self.play_sound('crash')
            raise "Hit the boundry error"

    # render the score of the current game
    def display_score( self ):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length - 1}",True,(200,200,200))
        self.surface.blit( score,(850,10) )


    # when you have died
    def show_game_over( self ):
        self.render_background()
        # show the score you had before you died
        font = pygame.font.SysFont( 'arial', 30 )
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        # render the score line
        self.surface.blit(line1, (200, 300))
        # show the options line where
        # Esc - for exit the whole game
        # Enter - start a new game
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        # render line2
        self.surface.blit( line2, (200, 350) )
        # stopping the background music 
        # when you die we don't want the 
        # music to continue playing 
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run( self ):
        running = True
        pause = False

        
        while running:
            # Events accoring to the event such as key strokes
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    # when you died and you want to 
                    # play again 
                    # we make the background music start playing
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    # if the game is still playing and not paused
                    # we want to use these events to control the snake
                    if not pause:
                        if event.key == K_LEFT:
                            if self.snake.direction != 'right':
                                self.snake.move_left()

                        if event.key == K_RIGHT:
                            if self.snake.direction != 'left':
                                self.snake.move_right()

                        if event.key == K_UP:
                            if self.snake.direction != 'down':
                                self.snake.move_up()

                        if event.key == K_DOWN:
                            if self.snake.direction != 'up':
                                self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            # Exceptions that are raised
            try:
                # if the game is in play mode
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)

if __name__ == '__main__':
    game = Game()
    game.run()