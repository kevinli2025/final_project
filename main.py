#File created by Kevin Li
#Sources: https://inventwithpython.com/blog/2012/07/18/using-trigonometry-to-animate-bounces-draw-clocks-and-point-cannons-at-a-target/
#Sources: https://stackoverflow.com/questions/45644916/pygame-remove-kill-sprite-after-time-period-without-polling

#import libraries
import random
import pygame as pg
from settings import *
from sprites import *

'''
objective: shoot all zombies on platforms with ricocheting bullet
'''

#Game class: main game for managing loops and sprites
class Game:
    #Initialize pygame and set up display
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Stupid Zombies Clone")
        self.clock = pg.time.Clock()
    #Start a new game
    def new(self):
        #Create a new gun, bullet group, platforms, and zombies
        self.gun = Gun((WIDTH // 2, HEIGHT - 30))
        self.bullets_group = pygame.sprite.Group()
        self.create_platforms_zombies()
        self.init_zombie_count = len(self.zombies)
        self.killed_zombies = 0
        self.bullets_left = MAX_BULLETS
        #Initialize game state to be "play"
        self.game_state = "play"
        #Kick off game loop
        self.run()

    #Randomly spawns platforms and zombies
    def create_platforms_zombies(self):    
        self.platforms = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        #Randomly spawns platforms within 200 pixels from the right to 200 pixels from the left
        #To prevent spawning too close to boundaries
        for i in range(INIT_ZOMBIE_COUNT):
            x = random.randint(200, WIDTH-200)
            y = random.randint(200, HEIGHT-300)
            self.platforms.add(Platform((x,y)))
            self.zombies.add(Zombie((x+100, y-5)))

    #Main game loop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)
            self.events()
            self.update()
        pg.quit()

    #Update interactions between zombies and bullets
    def update(self):
        #If the game is in the "play" state, update game elements
        if self.game_state == "play":
            #Update the gun's position and angle based on the mouse position
            self.gun.update(self.get_mouse_now())
            #Update bullets location
            self.bullets_group.update()
            self.bullets_group.draw(self.screen)
            #Displays images of platforms and zombies on screen
            for plat in self.platforms:
                self.screen.blit(plat.image, plat.rect)
            for zombie in self.zombies:
                self.screen.blit(zombie.image, zombie.rect)
            #Check for collisions between bullets and zombies
            #If a bullet hits a zombie, remove the zombie and increase the zombie kill count
            for bullet in self.bullets_group:
                hit_zombies = pg.sprite.spritecollide(bullet, self.zombies, False)
                if hit_zombies:
                    hit_zombies[0].kill()
                    self.killed_zombies += 1
            #If number of zombies killed is equal to original number of zombies, game_state is set to win
            #Else if bullets run out, game_state is set to lose
            if self.killed_zombies == self.init_zombie_count:
                self.game_state = "win"
            elif self.bullets_left == 0 and len(self.bullets_group) == 0:
                self.game_state = "lose"

        #Displays "win" or "lose" message if winning conditions are met/not met
        #Displays restart button to let user play again
        elif self.game_state == "win":
            self.draw_text(self.screen, "Good job!", (WIDTH // 2 - 50, HEIGHT // 2 - 20), FONT_SIZE, WHITE)
            self.button(self.screen, "Restart", (WIDTH // 2 - 50, HEIGHT // 2 + 20), (100, 30), GREEN, self.restart_game)
        elif self.game_state == "lose":
            self.draw_text(self.screen, "You failed!", (WIDTH // 2 - 50, HEIGHT // 2 - 20), FONT_SIZE, WHITE)
            self.button(self.screen, "Restart", (WIDTH // 2 - 50, HEIGHT // 2 + 20), (100, 30), RED, self.restart_game)

        self.gun.draw(self.screen)
        #Display number of bullets left
        self.draw_text(self.screen, str(self.bullets_left) + " bullets left", (20, HEIGHT-30), FONT_SIZE, WHITE)

        pg.display.flip()

    #Handle user events
    def events(self):
        for event in pg.event.get():
            #If user quits, end the game
            if event.type == pg.QUIT:
                self.playing = False

            #If user clicks mouse, shoot a new bullet
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.game_state == "play" and self.bullets_left > 0:
                    bullet = Bullet(self.gun.rect.center, self.gun.angle, self.screen, self.platforms, self.bullets_group)
                    #Decrease number of bullets left
                    #If no bullets left, end the game
                    if self.bullets_left > 0:
                        self.bullets_left -= 1
                    else: 
                        self.playing = False

    #Get mouse position
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)
    
    #Display text
    def draw_text(self, surface, text, pos, font_size, color):
        font = pg.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)    

    #Create a button to let user restart
    def button(self, surface, text, pos, size, color, action=None):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        pg.draw.rect(surface, color, (pos[0], pos[1], size[0], size[1]))
        if pos[0] < mouse[0] < pos[0] + size[0] and pos[1] < mouse[1] < pos[1] + size[1]:
            pg.draw.rect(surface, (255, 255, 0), (pos[0], pos[1], size[0], size[1]), 2)
            #If user clicks the button, call restart_game
            if click[0] == 1 and action is not None:
                action()
        else:
            pg.draw.rect(surface, (0, 0, 0), (pos[0], pos[1], size[0], size[1]), 2)

        self.draw_text(surface, text, (pos[0] + 5, pos[1] + 5), FONT_SIZE, WHITE)
        
    def restart_game(self):
        #Remove all bullets
        for bullet in self.bullets_group:
            bullet.kill()
        #Remove all platforms
        for plat in self.platforms:
            plat.kill()
        #Remove all zombies
        for zombie in self.zombies:
            zombie.kill()
        #Create a new game
        self.new()

#Instantiate the game class...
g = Game()
g.new()