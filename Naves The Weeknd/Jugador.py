import pygame, random

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load(r"C:\\Users\rockp\OneDrive\Documentos\assets/player.png").convert() #Aquí cargamos la imagen de nuestro personaje.
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0

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

#Aquí agregamos a los enemigos(Aliens).
class Aliens(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load(r"C:\\Users\rockp\OneDrive\Documentos\assets/Alien.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)


	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 10)

#Clase de las balas.
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load(r"C:\\Users\rockp\OneDrive\Documentos\assets/laser.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10
	
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()


# Cargar imagen de fondo (en caso de querer cambiar fondo modificar abajo)
background = pygame.image.load(r"C:\\Users\rockp\OneDrive\Documentos\assets/background.png").convert()

#Listas
all_sprites = pygame.sprite.Group()
aliens_list = pygame.sprite.Group()
bullets = pygame.sprite.Group

player = Player()
all_sprites.add(player)
for i in range(8):     #cantidad de Aliens.
	aliens = Aliens()
	all_sprites.add(aliens)
	aliens_list.add(aliens)

# Game Loop
running = True
while running:
	# Keep loop running at the right speed
	clock.tick(60)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:  #Aquí podemos cambiar la tecla del disparo.
				player.shoot()

	# Update
	all_sprites.update() 

	#Colisiones - Alien - laser.
	hits = pygame.sprite.groupcollide(aliens_list, bullets, True, True)
	for hit in hits:
		aliens = Aliens()
		all_sprites.add(aliens)
		aliens_list.add(aliens)

	#Colisiones - Jugador - Aliens
	hits = pygame.sprite.spritecollide(player, aliens_list, True)
	if hits:
		running = False



	#Draw / Render
	screen.blit(background, [0, 0])

	all_sprites.draw(screen)
	# *after* drawing everything, flip the display.
	pygame.display.flip()

pygame.quit()
