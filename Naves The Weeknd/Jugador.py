from __future__ import barry_as_FLUFL
from ctypes.wintypes import PLARGE_INTEGER
from logging import setLogRecordFactory
from operator import truediv
from platform import platform, python_branch
from tkinter import CENTER, font
from tkinter.tix import Meter
from tokenize import PlainToken
from turtle import width
import pygame, random
WIDTH = 800
HEIGHT = 600
WHITE=(255,255,255)
BLACK = (0, 0, 0)
GREEN=(0,255,0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

def draw_text(surface, text,size,x,y):
	font= pygame.font.SysFont("serif",size)
	text_surface=font.render(text,True,WHITE)
	text_rect=text_surface.get_rect()
	text_rect.midtop=(x,y)
	surface.blit(text_surface,text_rect)

def draw_shield_bar(surface,x,y,percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x,y, fill , BAR_HEIGHT)
	pygame.draw.rect(surface,GREEN,fill)
	pygame.draw.rect(surface, WHITE,border,2)


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load(r"C:\Users\Luis\Documents\assets/player.png").convert() #Aquí cargamos la imagen de nuestro personaje.
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.shield = 100

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	#Balas:
	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		laser_sound.play()

	

#Aquí agregamos a los enemigos(Aliens).
class Aliens(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(Meteor_imagenes)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-140, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)


	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 10)

#Clase de las balas.
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load(r"C:\Users\Luis\Documents\assets/laser.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10
	
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

 
Meteor_imagenes= []
Meteor_lista= [r"C:\\Users\Luis\Documents\pythongame-main\pythongame-main\Naves The Weeknd\assets/Alien2.png",
			r"C:\\Users\Luis\Documents\pythongame-main\pythongame-main\Naves The Weeknd\assets/Asteroide2.png",r"C:\\Users\Luis\Documents\pythongame-main\pythongame-main\Naves The Weeknd\assets/Asteroide.png",
			r"C:\\Users\Luis\Documents\pythongame-main\pythongame-main\Naves The Weeknd\assets/Alien.png"]
for img in Meteor_lista:
	Meteor_imagenes.append(pygame.image.load(img).convert())


#Explosiones#

# Cargar imagen de fondo (en caso de querer cambiar fondo modificar abajo)
background = pygame.image.load(r"C:\Users\Luis\Documents\assets/background.png").convert()


#Sonidos
laser_sound=pygame.mixer.Sound(r"C:\\Users\Luis\Documents\pythongame-main\pythongame-main\Naves The Weeknd\Sonido/LaserRapido.ogg")
explosion_sound=pygame.mixer.Sound(r"C:\\Users\Luis\Documents\pythongame-main\pythongame-main\Naves The Weeknd\Sonido/Explocion.wav")
pygame.mixer.music.load(r"C:\Users\Luis\Documents\pythongame-main\pythongame-main\Naves The Weeknd\Sonido\musica.mp3")
pygame.mixer.music.set_volume(0.6)


#Listas
all_sprites = pygame.sprite.Group()
aliens_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
for i in range(8):     #cantidad de Aliens.
	aliens = Aliens()
	all_sprites.add(aliens)
	aliens_list.add(aliens)


score=0
pygame.mixer.music.play(loops=-1)


# Game Loop
running = True
while running:
	clock.tick(60) 	# Keep loop running at the right speed
	for event in pygame.event.get(): # Process input (events)
		if event.type == pygame.QUIT: # check for closing window
			running = False
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:  #Aquí podemos cambiar la tecla del disparo.
				player.shoot()

	
	all_sprites.update() # Update

	#Colisiones - Alien - laser.
	hits = pygame.sprite.groupcollide(aliens_list, bullets, True, True)
	for hit in hits:
		score+=10
		explosion_sound.play()
		aliens = Aliens()
		all_sprites.add(aliens)
		aliens_list.add(aliens)

	#Colisiones - Jugador - Aliens
	hits = pygame.sprite.spritecollide(player, aliens_list, True)
	for hit in hits:
		player.shield -=25
		aliens = Aliens()
		all_sprites.add(aliens)
		aliens_list.add(aliens)
		if player.shield<= 0:
			running = False



	#Draw / Render
	screen.blit(background, [0, 0])
	#marcador
	draw_text(screen, str(score),25,30,13)

	all_sprites.draw(screen)
	# *after* drawing everything, flip the display.

	#Escudo
	draw_shield_bar(screen, 5, 5,player.shield)

	pygame.display.flip()
pygame.quit()
