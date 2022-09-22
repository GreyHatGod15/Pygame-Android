import sys
import pygame
from pygame.locals import *
import random

pygame.init()
# Resolution is ignored on Android
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
surfrect = screen.get_rect()

class Player():
	def __init__(self, x, y):
		self.touched = False
		self.x = x
		self.y = y
		self.color = (255,255,255)
		self.surf = pygame.Surface((100,100))
		self.surf.fill(self.color)
		self.rect = self.surf.get_rect()
		self.touched = False
		self.bullets = []
	
	def update(self):
		self.surf.fill(self.color)
		self.rect = pygame.rect.Rect((self.x, self.y, 100,100))
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()
				quit()
			if e.type == pygame.MOUSEBUTTONDOWN:
				if self.rect.collidepoint(e.pos):
					self.touched = True
					pygame.mouse.get_rel()
			elif e.type == pygame.MOUSEBUTTONUP:
				self.touched = False
		if self.touched:
			self.color = (255,0,0)
			relx, rely = pygame.mouse.get_rel()
			self.x += relx
		elif not self.touched:
			self.color = (255,255,255)
		if frame == 1:
			self.bullets.append(PlayerBullet(self.x+40, self.y))
		for bullet in self.bullets:
			bullet.update()
		screen.blit(self.surf, (self.x, self.y))


class PlayerBullet():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.color = (200,200,0)
		self.surf = pygame.Surface((20, 30))
		self.surf.fill(self.color)
		self.yvel = 50
		self.id = len(player.bullets) * random.randint(3,99)
	
	def update(self):
		self.surf.fill(self.color)
		self.rect = pygame.rect.Rect((self.x, self.y, 20, 30))
		self.y -= self.yvel
		screen.blit(self.surf, (self.x, self.y))
		if self.y < -10:
			player.bullets.remove(self)
			del self

class Enemy():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 70
		self.height = 70
		self.color = (0,200,0)
		self.surf = pygame.Surface((self.width, self.height))
		self.surf.fill((self.color))
		self.moving_down = False
		self.moving_init_y = 0
		self.xvel = 5
		self.colliding_bullet = False
		self.health = 2
		self.prev_coll = None
	
	def update(self):
		self.surf.fill((self.color))
		self.rect = pygame.rect.Rect((self.x, self.y, self.width, self.height))
		
		if self.moving_down:
			self.y += 5
			if self.y > self.moving_init_y + 100:
				self.moving_down = False
				self.xvel =-self.xvel
		if not self.moving_down:
			self.x += self.xvel
			if self.x > surfrect.width-self.width-10:
				self.moving_init_y = self.y
				self.moving_down = True
			if self.x < 10:
				self.moving_init_y = self.y
				self.moving_down = True
		for bullet in player.bullets:
			if bullet.rect.colliderect(self.rect):
				if not bullet.id == self.prev_coll:
					self.health -= 1
					self.prev_coll = bullet.id
					player.bullets.remove(bullet)
					self.colliding_bullet = True
					self.prev_coll = None
					
		if self.health <= 0:
			enemies.remove(self)
			temp = []
			for i in range(random.randint(50,70)):
				temp.append(Particle(self.x+45, self.y+45))
			particles.append(temp)
		if self.colliding_bullet:
			self.surf.fill((255,0,0))
		screen.blit(self.surf, (self.x, self.y))

class Particle():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.xvel, self.yvel = (random.randint(-15,15), random.randint(-15,15))
		self.color = random.choice([(255,200,0), (255,255,255), (70,70,70)])
		self.radius = random.randint(3,16)
	
	def update(self):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
		self.x += self.xvel
		self.y += self.yvel

particles = []
aim_assist = pygame.Surface((20,surfrect.height-100))
aim_assist.fill((255,255,255))
aim_assist.set_alpha(50)
frame = 0
frame_count = 0
en_frame = 0
player = Player(surfrect.width/2-50, surfrect.height-200)
enemies = []
touched = False
while True:
	frame += 1
	en_frame += 1
	if frame >= 40:
		frame = 1
		frame_count += 1
	if frame_count >= 4:
		frame_count = 0
	if en_frame >= 90:
		enemies.append(Enemy(10,10))
		en_frame = 0
	screen.fill((0,0,0))
	player.update()
	for enemy in enemies:
		enemy.update()
	for particle_group in particles:
		for particle in particle_group:
			particle.update()
			if particle.x < 0 or particle.x > surfrect.width:
				particle_group.remove(particle)
			elif particle.y < 0 or particle.y > surfrect.height:
				particle_group.remove(particle)
		if particle_group == []:
			particles.remove(particle_group)
	screen.blit(aim_assist, (player.x+40, -100))
	pygame.display.update()
	clock.tick(60)