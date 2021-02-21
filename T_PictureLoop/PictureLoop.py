import pygame
import time
import os
import random
 
number = 1
T = 0.5
screen = pygame.display.set_mode((440,280),0,32)
screen.fill((255,255,255))
background=pygame.image.load("images/bg.jpg")  #Picture location   while True:   #Loop Update
screen.blit(background,(0,0))
myimage=pygame.image.load("images/L.png")
screen.blit(myimage,[0,50])
myimage=pygame.image.load("images/R.jpg")
screen.blit(myimage,[275,50])
myimage=pygame.image.load("images/10.png") ##Assign the variable myimage to the imported image
screen.blit(myimage,[156,178])
pygame.display.update()   #Display
def Show_Photo(string):
	background=pygame.image.load(string)  #Picture location   while True:   #Loop Update
	screen.blit(background,(124.5,50))
	pygame.display.update()   #Display
while(1):
	for event in pygame.event.get():#Get Event
		if event.type==pygame.MOUSEBUTTONDOWN:
			while(1):
				num = random.randint(1,8)
				if str(num) == "1":
					Show_Photo("images/1.png")
				if str(num) == "2":
					Show_Photo("images/2.png")
				if str(num) == "3":
					Show_Photo("images/3.png")
				if str(num) == "4":
					Show_Photo("images/4.png")
				if str(num) == "5":
					Show_Photo("images/5.png")
				if str(num) == "6":
					Show_Photo("images/6.png")
				if str(num) == "7":
					Show_Photo("images/7.png")
				if str(num) == "8":
					Show_Photo("images/8.png")
				if str(num) == "9":
					Show_Photo("images/9.png")
				
				
				time.sleep(T)
				number = number + 1
				if number % 5 == 0:
					T = T - 0.1
				if number == 20:
					string = str(num) + ".png"
					print (string)
					break
while(1):
	Show_Photo(string)
