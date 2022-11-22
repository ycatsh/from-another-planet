import pygame, sys
from pygame.locals import *
import random, math

clock = pygame.time.Clock()

pygame.init()

windowSize = (1200, 800)
window = pygame.display.set_mode((windowSize), pygame.NOFRAME, vsync=1)

#icons
icon = pygame.image.load('assets/icon.png').convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("From Another Planet")

#fonts C&C Red Alert [INET]
menuFont = pygame.font.Font("assets/fonts/font.ttf", 100)
font = pygame.font.Font("assets/fonts/font.ttf", 60) 
font2 = pygame.font.Font("assets/fonts/font.ttf", 40)
font3 = pygame.font.Font("assets/fonts/font.ttf", 30)

mColor = (110, 69, 206)
def menu(text, font, mColor, x, y):
	m = font.render(text, True, mColor)
	window.blit(m, (x,y))


lvl = 1
nA = 4 #number of aliens every level; level 1: 4
n_bA = 2 #number of blue aliens every level
n_hP = 0 #number of health pots 

alienList = []
blue_alienList = []
laserList = []
aliensKilled = 0
rockList = []

#cursor 
cursor = pygame.image.load('assets/cursor.png').convert_alpha()

#backgrounds
bg = pygame.image.load('assets/bg.png').convert_alpha()
start_bg = pygame.image.load('assets/start_bg.png').convert_alpha()
start_bg2 = pygame.image.load('assets/start_blur.png').convert_alpha()
menu_bg = pygame.image.load('assets/menu_bg.png').convert_alpha()
over_bg = pygame.image.load('assets/over_bg.png').convert_alpha()

#player and enemy
p = pygame.image.load('assets/p.png').convert_alpha()
a = pygame.image.load('assets/aliens/a1.png').convert_alpha()
a2 = pygame.image.load('assets/aliens/a2.png').convert_alpha()

#bullet
b = pygame.image.load('assets/bullet.png').convert_alpha()

#laser
l1 = pygame.image.load('assets/laser1.png').convert_alpha()
l2 = pygame.image.load('assets/laser2.png').convert_alpha()

rockRandom = []
for i in range(1,7):
	rockChoose = pygame.image.load(f'assets/rocks/r{i}.png').convert_alpha()
	rockRandom.append(rockChoose)

class Button():
	def __init__(self, image, x, y):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.click = False 

	def draw(self):
		action = False 
		mXY = pygame.mouse.get_pos()

		if self.rect.collidepoint(mXY):
			if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
				self.click = True
				action = True

			if pygame.mouse.get_pressed()[0] == 0:
				self.click = False 

		window.blit(self.image, (self.rect.x, self.rect.y))

		return action 

#buttons
bP = pygame.image.load('assets/resume_button.png').convert_alpha()
bQ = pygame.image.load('assets/quit_button.png').convert_alpha()
playButton = Button(bP, 590, 420)
quitButton = Button(bQ, 590, 530)
play_overButton = Button(bP, 600, 450)
quit_overButton = Button(bQ, 600, 530)
play_pauseButton = Button(bP, 600, 430)
quit_pauseButton = Button(bQ, 600, 520)

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, scale, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(p, (int(p.get_width()*scale), p.get_height() * scale))
		self.lives = 6
		self.flip = False
		self.directionx = 0
		self.directiony = 0
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.location = location
		self.rate = 0

	def update(self):
		if self.rate > 0:
			self.rate -= 1

		collisionsAlien = pygame.sprite.spritecollide(self, alienList, False)
		for h in collisionsAlien:      
			if self.lives != 0:  
				self.lives -= 1
				self.kill()

		collisionsBlue = pygame.sprite.spritecollide(self, blue_alienList, False)
		for i in collisionsBlue:
			if self.lives != 0:  
				self.lives -= 1
				self.kill()

		collisionsRock = pygame.sprite.spritecollide(self, rockList, False)
		for j in collisionsRock:      
			if self.lives != 0:  
				self.lives -= 6
				self.kill()

		collisionsLaser = pygame.Rect.colliderect(self.rect, laser.rect)
		if collisionsLaser:
			#print(log.pos, self.rect.y) 
			if self.rect.y < laser.pos - 48 or self.rect.y > laser.pos + 48:
				if self.lives != 0:  
					self.lives -= 1
					self.kill()
			else:
				pass

	def move(self, moveR, moveL, moveU, moveD):
		x = 0
		y = 0

		if moveR: 
			x = self.location
			self.directionx = 1
			self.flip = True
			y = 0
		if moveL:
			x = -self.location
			self.directionx = -1
			self.flip = False 
			y = 0
		if moveU: 
			y = -self.location
			self.directiony = 1
			self.flip = True
			x = 0
		if moveD:
			y = self.location
			self.directiony = -1
			self.flip = False
			x = 0
			
		if self.rect.bottom + y > 740:
			y = 740 - self.rect.bottom
		
		if self.rect.top + y < 65:
			y = 5

		if self.rect.left + x > 1080:
			x = 1080 - self.rect.left

		if self.rect.right + x <= 120:
			x = 120 - self.rect.right
		
		self.rect.x += x
		self.rect.y += y      

	def shoot(self):
		if self.rate == 0:
			self.rate = 25
			global bullet 
			bullet = Bullet(self.rect.centerx+(40*self.directionx), self.rect.centery+(5*self.directiony),self.directionx)
			bulletGroup.add(bullet)

	def show(self):
		window.blit(pygame.transform.flip(self.image, self.flip, self.flip), self.rect)

player = Player(600, 400, 1, 4)

lives = []
for x in range(7):
	healthImage = pygame.image.load(f'assets/health/{x}.png').convert_alpha()
	lives.append(healthImage)

class HealthBar():
	def __init__(self, image, x, y, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)

	def show(self):
		window.blit(lives[player.lives], (self.rect.x, self.rect.y))

HEALTH = HealthBar(lives[player.lives], 560, 755, 0.7)

class Alien(pygame.sprite.Sprite):
	def __init__(self, x, y, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = a
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.location = location
		self.speed = 2

	def move(self):
		self.rect.x -= self.speed
	
	def update(self): 
		global aliensKilled 

		collisionsBullet = pygame.sprite.spritecollide(self, bulletGroup, False)

		for k in collisionsBullet:   
			if player.lives > 0:
				self.kill()
				alienList.remove(alien) 
				bulletGroup.remove(bullet)
				aliensKilled += 1

		collisionsRock = pygame.sprite.spritecollide(self, rockList, False)
		for j in collisionsRock:      
				self.kill()
				alienList.remove(self) 

	def show(self):
		window.blit(self.image, (self.rect.x, self.rect.y))

for j in range(nA):
	alien = Alien(random.randint(1400, 1600), (random.randint(90, 680)), 3)
	alienList.append(alien)

class BlueAlien(pygame.sprite.Sprite):
	def __init__(self, x, y, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = a2
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.location = location
		self.speed = 3
		self.chance = random.randint(1,5)

	def move(self):
		if self.chance == 2:
			self.rect.x -= self.speed
	
	def update(self):
		if self.chance == 2:
			global aliensKilled 

			collisions_blueBullet = pygame.sprite.spritecollide(self, bulletGroup, False)

			for l in collisions_blueBullet: 
				if player.lives > 0:  
					self.kill()
					blue_alienList.remove(alienBlue) 
					bulletGroup.remove(bullet)
					aliensKilled += 1

			collisionsRock = pygame.sprite.spritecollide(self, rockList, False)
			for m in collisionsRock:      
				self.kill()
				blue_alienList.remove(self) 

	def show(self):
		if self.chance == 2:
			window.blit(self.image, (self.rect.x, self.rect.y))

for k in range(n_bA):
	alienBlue = BlueAlien(random.randint(1400, 1600), (random.randint(90, 680)), 3)
	blue_alienList.append(alienBlue)

class Laser(pygame.sprite.Sprite):
	def __init__(self, x, y, location):
		pygame.sprite.Sprite.__init__(self)
		#self.sprites = [] #disabling animation for now
		#self.sprites.append(l1)
		#self.sprites.append(l2)
		#self.current_sprite = 0
		#self.image = self.sprites[self.current_sprite]
		self.image = l1
		self.image2 = pygame.image.load('assets/opening.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect2 = self.image2.get_rect()
		self.rect.center = (x,y)
		self.rect2.center = (x,y)
		self.location = location
		self.speed = 2
		self.pos = random.randint(200, 560) 

	def update(self):
		self.speed += lvl/10

	def moveLR(self):
		self.rect.x += self.speed
		self.rect2.x += self.speed

	def moveRL(self): 
		self.rect.x = (self.rect.x *-1) + self.speed
		self.rect2.x = (self.rect2.x *-1) + self.speed
		self.pos = random.randint(200, 560)
		
	def show(self):
		#disabling animation for now
		#self.current_sprite += 0 
		#if self.current_sprite > 1:
			#self.current_sprite = 0
		#self.image = self.sprites[int(self.current_sprite)]
		window.blit(self.image, (self.rect.x, self.rect.y))
		window.blit(self.image2, (self.rect2.x, self.pos))

laser = Laser(1, 400, 3)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, directionx):
		pygame.sprite.Sprite.__init__(self)
		self.image = b
		self.directionx = directionx
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.speed = 10

	def update(self):
		self.rect.x += (self.directionx * self.speed)

		if self.rect.right < 95 or self.rect.left > 1105:
			#print(self.rect.right)
			#print(self.rect.left)
			self.kill()

bulletGroup = pygame.sprite.Group()

class Rock(pygame.sprite.Sprite):
	def __init__(self, x, y, location, angle):
		pygame.sprite.Sprite.__init__(self)
		self.image = random.choice(rockRandom)
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.velocity = random.randint(1,6)
		self.location = location
		self.chanceV = random.randint(1, 2)
		self.angle = 0
		self.rotate(angle)

	def update(self):
		x = 0 
		y = 0

		if self.chanceV == 1: 
			y = -self.location

			x = self.location


		if self.chanceV == 2:
			y = self.location

			x = self.location

		if self.rect.y + y > 1300:
			self.rect.y = -100
		
		self.rect.x += x
		self.rect.y += y

	def rotate(self, angle):
		self.rockSurface = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.rockSurface.get_rect(center = self.rect.center)

	def show(self):
		if rock.rect.x < 1300 and rock.rect.x > -100 and rock.rect.y > 50 and rock.rect.y < 700:
			window.blit(self.image, (self.rect.x, self.rect.y))

for i in range(1,6):
	x = random.randint(-1000, 1300)
	y = random.randint(1000, 1300)

	rock = Rock(x, y, 2, 45)
	rockList.append(rock)

	if x <= 600+100 and x >= 600-100 and y <= 400+100 and y >= 400-100:
		x += random.randint(120, 140)
		y += random.randint(120, 140)
		rock = Rock(x, y, random.randint(1,3), 45)
		rockList.append(rock)

playerTurn = False

#game loop
def main():
 
	global lvl, nA, n_bA, alienList, blue_alienList, health_potList, aliensKilled, alien, alienBlue, laser, player, laserNUM, rock

	#game variables
	gamePause = False 
	gameOver = False
	gameStart = False 

	tiles = math.ceil(1200 / bg.get_width()) + 1
	scroll = 0

	moveR = False
	moveL = False
	moveU = False
	moveD = False
	shoot = False

	while True: 

		if gameStart == False:
			window.blit(start_bg2, (0, 0))
			menu("FROM ANOTHER WORLD", font, mColor, 360, 270)

			if playButton.draw():
				gameStart = True

			if quitButton.draw():
				pygame.quit()
				sys.exit()

		if gameOver == True: 
			gameStart = False
			window.blit(over_bg, (0, 0))
			menu("YOU DIED...", font, mColor, 500, 250)
			menu("GAME OVER", font, mColor, 480, 330)

			#if play_overButton.draw():
				#gameStart = True

			if quit_overButton.draw():
				pygame.quit()
				sys.exit()

		if gamePause == True:
			if gameOver == True:
				pass
			else:
				window.blit(menu_bg, (0, 0))
				menu("PAUSE MENU", font, mColor, 470, 300)

				if play_pauseButton.draw():
					gamePause = False

				if quit_pauseButton.draw():
					pygame.quit()
					sys.exit()

		if gameStart == True and gamePause == False:

			for i in range(0, tiles):
				window.blit(bg, (i*bg.get_width() + scroll, 0))

			scroll -= 5
			if abs(scroll) > bg.get_width(): 
				scroll = 0

			clock.tick()
			menu(f"FPS: {int(clock.get_fps())}", font3, mColor, 75, 20)

			HEALTH.show()
		
			menu(f"ALIENS KILLED: {aliensKilled}", font3, mColor, 935, 747)
			menu(f"LEVEL: {lvl}", font3, mColor, 100, 747)

			if len(alienList) == 0:
				lvl += 1
				nA += 1
				n_bA += 1

				for j in range(nA):
					alien = Alien(random.randint(1400, 1600), (random.randint(90, 680)), 2)
					alienList.append(alien)

				for k in range(n_bA):
					alienBlue = BlueAlien(random.randint(1400, 1600), (random.randint(90, 680)), 3)
					blue_alienList.append(alienBlue)
				
				laser.update()

			laser.show()
			laser.moveLR()
			if laser.rect2.x >= 1200 and laser.rect.x >= 1200:
				laser.moveRL()
				#print(log.rect.x, log.rect2.x)

			for rock in rockList: 
				rock.show()
				rock.update()
				rock.rotate(45)

				if player.lives > 0:

					if len(rockList) < 3: 
						for i in range(1,6):
							x = random.randint(-1000, 1300)
							y = random.randint(1000, 1500)

							rock = Rock(x, y, random.randint(1,3), 45)
							rockList.append(rock)

							if x <= 600+100 and x >= 600-100 and y <= 400+100 and y >= 400-100:
								x += random.randint(120, 140)
								y += random.randint(120, 140)
								rock = Rock(x, y, random.randint(1,3), 45)
								rockList.append(rock)

				if rock.rect.x > 2000 or rock.rect.x < -100 and rock.rect.y > 2000 or rock.rect.y < -100:
					rockList.remove(rock)


			bulletGroup.draw(window)
			bulletGroup.update()

			player.update()
			player.show()
			player.move(moveR, moveL, moveU, moveD)

			for alien in alienList:
				alien.show()
				alien.update()
				alien.move()
				if player.lives > 0:
					if alien.rect.x + alien.image.get_width() < 64: 
							player.lives -= 1
							alienList.remove(alien)

			for alienBlue in blue_alienList:
				alienBlue.show()
				alienBlue.update()
				alienBlue.move()

				if player.lives > 0:
					if alienBlue.rect.x + alienBlue.image.get_width() < 64: 
						player.lives -= 1
						blue_alienList.remove(alienBlue)

			if player.lives <= 6 and player.lives > 0:
				if shoot: 
					comb = []
					comb.append(player.directionx)
					comb.append(player.directiony)
					#print(comb) 
					player.shoot()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
			if player.lives <= 0:
				gameOver = True
				gameStart = False

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					gamePause = True
				if event.key == K_SPACE:
					shoot = True
				if event.key == K_RIGHT or event.key == K_d:
					moveR = True
				if event.key == K_LEFT or event.key == K_a:
					moveL = True
				if event.key == K_UP or event.key == K_w:
					moveU = True
				if event.key == K_DOWN or event.key == K_s:
					moveD = True

			if event.type == KEYUP:
				if event.key == K_SPACE:
					shoot = False
				if event.key == K_RIGHT or event.key == K_d:
					moveR = False
				if event.key == K_LEFT or event.key == K_a:
					moveL = False
				if event.key == K_UP or event.key == K_w:
					moveU = False
				if event.key == K_DOWN or event.key == K_s:
					moveD = False

		pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
		cX,cY = pygame.mouse.get_pos()
		pos = [cX, cY]
		window.blit(cursor, pos)
		
		pygame.display.update()
		clock.tick(60)

main()