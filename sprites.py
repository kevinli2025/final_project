from settings import *
import pygame
import math
pygame.mixer.init()

# Sounds
ZOMBIEKILL_SOUND = pygame.mixer.Sound('sounds/zombiekill.mp3')
BULLETBOUNCE_SOUND = pygame.mixer.Sound('sounds/bounce.mp3')
GUNFIRING_SOUND = pygame.mixer.Sound('sounds/firing.mp3')

#load images for sprites
gun_img = pygame.image.load("images/gun.png")
zombie_img = pygame.image.load("images/zombie.png")
#platform_img = pygame.image.load("images/platform.png")

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, screen, platforms, *groups):
        super().__init__(*groups)
        
        self.screen = screen
        self.platforms = platforms
        #Initialize the angle of the bullet direction
        self.angle = math.radians(angle)
        self.vel = pygame.math.Vector2(BULLET_SPEED * math.cos(self.angle), -BULLET_SPEED * math.sin(self.angle))
        x = pos[0] + self.vel.x * 10
        y = pos[1] + self.vel.y * 10
        self.pos = pygame.math.Vector2((x,y))
        self.bounces = 0
        #Bullet's appearance
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x,y))
        GUNFIRING_SOUND.play()

    def update(self):
        #Updates position based on velocity
        self.pos += self.vel
        self.rect.topleft = self.pos
        #if bullet bounces more than maximum, it disappears
        if self.bounces >= MAX_BOUNCES:
            self.kill()
        #Check if the bullet hits the screen boundaries, if so, bounce it back
    
        if not self.rect.colliderect(self.screen.get_rect()):
            self.bounces += 1
            if self.rect.left < 0:
                self.pos.x = 0
                self.vel.x *= -1
                BULLETBOUNCE_SOUND.play()    
            if self.rect.right > WIDTH:
                self.pos.x = WIDTH - self.rect.width
                self.vel.x *= -1
                BULLETBOUNCE_SOUND.play()    
            if self.rect.top < 0:
                self.pos.y = 0
                self.vel.y *= -1
                BULLETBOUNCE_SOUND.play()    
            if self.rect.bottom > HEIGHT:
                self.pos.y = HEIGHT - self.rect.height
                self.vel.y *= -1
                BULLETBOUNCE_SOUND.play()    

        


        #Check for collisions with platforms and update bounces accordingly
        for platform in self.platforms:
            if platform.rect.collidepoint(self.pos.x, self.pos.y):
                # Determine collision direction
                if abs(self.pos.x - platform.rect.right) < 5 or abs(self.pos.x - platform.rect.left) < 5:
                    self.vel.x *= -1
                    self.bounces += 1
                    BULLETBOUNCE_SOUND.play()    
                elif abs(self.pos.y - platform.rect.bottom) < 5 or abs(self.pos.y - platform.rect.top) < 5:
                    self.vel.y *= -1
                    self.bounces += 1
                    BULLETBOUNCE_SOUND.play()    

            




#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, *groups):
        super().__init__(*groups)
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#zombie class
class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = zombie_img
        self.rect = self.image.get_rect(midbottom=pos)
#gun class
class Gun:
    def __init__(self, pos):
        self.pos = pos
        self.angle = 0
        self.image = gun_img
        self.original_image = gun_img

    def update(self, mouse_pos):
        #Calculate the angle of the gun based on mouse position
        dx, dy = mouse_pos[0] - self.pos[0], self.pos[1] - mouse_pos[1]
        r = math.sqrt(dx*dx + dy*dy)
        self.angle = math.acos(dx/r) / math.pi * 180
        #Rotate the gun accordingly
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)