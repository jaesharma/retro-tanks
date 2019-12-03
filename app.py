import pygame
import time
import random
import threading
import sys

pygame.init()

introbg=pygame.image.load('imgs/introbg.jpg')
gameoverim=pygame.image.load('imgs/gameover.png')
mainbg=pygame.image.load('imgs/mainbg.jpg')
base=pygame.image.load('imgs/baseimg.png')

blue=(0,0,255)
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
lightered=(150,0,0)
green=(0,255,0)
lightergreen=(0,150,0)
yellow=(120,150,0)
lighteryellow=(80,120,0)
screenWidth=800
screenHeight=600
ground=34
explosion_sound=pygame.mixer.Sound('exp.wav')
pygame.display.set_caption("The Tanks")

gameDisplay=pygame.display.set_mode((screenWidth,screenHeight))

fps=60
tankHeight=20
tankWidth=40
turretWidth=3
wheelWidth=5
clock=pygame.time.Clock()

smallfont=pygame.font.SysFont('comicsansms',25)
midfont=pygame.font.SysFont('comicsansms',35)
largefont=pygame.font.SysFont('comicsansms',45)


def textObject(msg,color,size="small"):
	if size=="small":
		textsurf=smallfont.render(msg,True,color)
	elif size=="mid":
		textsurf=midfont.render(msg,True,color)
	elif size=="large":
		textsurf=largefont.render(msg,True,color)
	return textsurf,textsurf.get_rect()

def button(text,color,x,y,w,h,action=None):
	click=pygame.mouse.get_pressed()
	pygame.draw.rect(gameDisplay,color,(x,y,w,h))
	textsurf,textrect=textObject(text,color=black,size="small")
	textrect.center=((x+(w/2)),(y+(h/2)))
	gameDisplay.blit(textsurf,textrect)
	if click[0]==1 and action is not None:
		if action=="play":
			gameloop()
		if action=="main":
			intro()
		if action=="controls":
			controls()
		if action=="quit":
			pygame.quit()
			quit()

def displaymsg(msg,color,ydisplace,size):
	surftext,textrect=textObject(msg,color,size)
	textrect.center=(screenWidth/2),(screenHeight/2)+ydisplace
	gameDisplay.blit(surftext,textrect)

def barrier(x,y,width):
	pygame.draw.rect(gameDisplay,black,(x,screenHeight-y,width,y))

def explosion(x,y,size):
	# pygame.mixer.Sound.play(explosion_sound)
	colors=[red,yellow,lightered,green,lightergreen]
	magnitude=1
	while magnitude<size:
		exploiding_bit_x=x+random.randrange(-1*magnitude,magnitude)
		exploiding_bit_y=y+random.randrange(-1*magnitude,magnitude)
		pygame.draw.circle(gameDisplay,colors[random.randrange(0,5)],(exploiding_bit_x,exploiding_bit_y),random.randrange(1,5))
		magnitude+=1
		pygame.display.update()
		clock.tick(100)
	return


def efireShell(xy,etankx,etanky,turpos,shellpow,xloc,barrierHeight,barrierwidth,tankX,tankY):
	fire=True
	shellpointer=list(xy)
	damage=0
	while fire:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()

		check_x1=shellpointer[0]<=xloc+barrierwidth
		check_x2=shellpointer[0]>=xloc
		check_y1=shellpointer[1]>=screenHeight-barrierHeight
		check_y2=shellpointer[1]<=screenHeight

		if check_x1 and check_x2 and check_y1 and check_y2:
			explosion(shellpointer[0],shellpointer[1],50)
			fire=False

		if shellpointer[1]>screenHeight-ground:
			explosion(shellpointer[0],screenHeight-ground,50)
			fire=False

		if tankY<=shellpointer[1]<=tankY+20 and tankX-20<=shellpointer[0]<=tankX+30:
			damage=15
		elif tankY<=shellpointer[1]<=tankY+20 and tankX-30<=shellpointer[0]<=tankX+40:
			damage=6
		elif tankY<=shellpointer[1]<=tankY+20 and tankX-35<=shellpointer[0]<=tankX+45:
			damage=3
		pygame.draw.circle(gameDisplay,red,(shellpointer[0],shellpointer[1]),5)
		shellpointer[0]+=(12-turpos)*2
		gun_power=random.randrange(int(shellpow*0.90),int(shellpow*1.10))
		shellpointer[1]+=int((((shellpointer[0]-xy[0])*0.015/(gun_power/50))**2)-(turpos+turpos/(12-turpos)))		
		pygame.display.update()
		clock.tick(100)
	return damage

def fireShell(xy,tankx,tanky,turpos,shellpow,xloc,barrierHeight,barrierwidth,etankX,etankY):
	fire=True
	shellpointer=list(xy)
	damage=0
	while fire:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()

		check_x1=shellpointer[0]<=xloc+barrierwidth
		check_x2=shellpointer[0]>=xloc
		check_y1=shellpointer[1]>=screenHeight-barrierHeight
		check_y2=shellpointer[1]<=screenHeight

		if check_x1 and check_x2 and check_y1 and check_y2:
			explosion(shellpointer[0],shellpointer[1],50)
			fire=False

		if shellpointer[1]>screenHeight-ground:
			explosion(shellpointer[0],screenHeight-ground,50)
			fire=False

		if etankY<=shellpointer[1]<=etankY+20 and etankX-20<=shellpointer[0]<=etankX+30:
			damage=15
		elif etankY<=shellpointer[1]<=etankY+20 and etankX-30<=shellpointer[0]<=etankX+40:
			damage=6
		elif etankY<=shellpointer[1]<=etankY+20 and etankX-35<=shellpointer[0]<=etankX+45:
			damage=3
		pygame.draw.circle(gameDisplay,red,(shellpointer[0],shellpointer[1]),5)
		shellpointer[0]-=(12-turpos)*2
		shellpointer[1]+=int((((shellpointer[0]-xy[0])*0.015/(shellpow/50))**2)-(turpos+turpos/(12-turpos)))
		pygame.display.update()
		clock.tick(100)
	return damage

def tank(x,y,turretindex):
	x=int(x)
	y=int(y)
	turretpos=[(x-26,y-3),(x-26,y-8),(x-24,y-11),(x-22,y-13),(x-22,y-15),(x-21,y-16),(x-19,y-18),(x-18,y-20),(x-16,y-21)]
	pygame.draw.circle(gameDisplay,black,(x,y),int(tankHeight/2))
	pygame.draw.rect(gameDisplay,black,(x-tankHeight,y,tankWidth,tankHeight))
	pygame.draw.line(gameDisplay,black,(x,y),turretpos[turretindex],turretWidth)
	startw=15
	for i in range(7):
		pygame.draw.circle(gameDisplay,black,(x-startw,y+22),wheelWidth)
		startw-=5
	return turretpos[turretindex]

def enemy_tank(x,y,turretindex):
	x=int(x)
	y=int(y)
	turretpos=[(x+26,y-3),(x+26,y-8),(x+24,y-11),(x+22,y-13),(x+22,y-15),(x+21,y-16),(x+19,y-18),(x+18,y-20),(x+16,y-21)]
	pygame.draw.circle(gameDisplay,black,(x,y),int(tankHeight/2))
	pygame.draw.rect(gameDisplay,black,(x-tankHeight,y,tankWidth,tankHeight))
	pygame.draw.line(gameDisplay,black,(x,y),turretpos[turretindex],turretWidth)
	startw=15
	for i in range(7):
		pygame.draw.circle(gameDisplay,black,(x-startw,y+22),wheelWidth)
		startw-=5
	return turretpos[turretindex]

def handlepower(power):
	powertext=smallfont.render(f"Power: {str(power)}%",True,black)
	gameDisplay.blit(powertext,[(screenWidth/2)-50,0])

def intro():
	while True:
		gameDisplay.blit(introbg,(0,0))
		pointer_pos=pygame.mouse.get_pos()
		if 150+100 > pointer_pos[0] >150 and 500+50 > pointer_pos[1] >500:
			button("play",green,140,490,110,60,action="play")
		else:
			button("play",lightergreen,150,500,100,50)
		if 350+100 > pointer_pos[0] >350 and 500+50 > pointer_pos[1] >500:
			button("controls",yellow,340,490,110,60,action="controls")
		else:
			button("controls",lighteryellow,350,500,100,50)
		if 550+100 > pointer_pos[0] >550 and 500+50 > pointer_pos[1] >500:
			button("quit",red,540,490,110,60,action="quit")
		else:
			button("quit",lightered,550,500,100,50)

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
		pygame.display.update()
		clock.tick(15)

def controls():
	while True:
		gameDisplay.blit(introbg,(0,0))
		displaymsg("CONTROLS",green,ydisplace=-120,size="large")
		displaymsg("Move Turret: Up and Down arrows",black,ydisplace=-60,size="mid")
		displaymsg("Move Tank: Left and Right arrows",black,ydisplace=0,size="mid")
		displaymsg("Press P to pause",black,ydisplace=60,size="mid")
		pointer_pos=pygame.mouse.get_pos()
		click=pygame.mouse.get_pressed()
		if 150+100 > pointer_pos[0] >150 and 500+50 > pointer_pos[1] >500:
			button("play",green,140,490,110,60,action="play")
		else:
			button("play",lightergreen,150,500,100,50)
		if 550+100 > pointer_pos[0] >550 and 500+50 > pointer_pos[1] >500:
			button("quit",red,540,490,110,60,action="quit")
		else:
			button("quit",lightered,550,500,100,50)
		pygame.display.update()

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()

		clock.tick(fps)

def pause():
	while True:
		displaymsg("Paused",green,ydisplace=-70,size="large")
		displaymsg("Press c to continue",black,ydisplace=-10,size="mid")
		displaymsg("Press q to quit",black,ydisplace=15,size="mid")
		for event in pygame.event.get():
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_q:
					pygame.quit()
					quit()
				if event.key==pygame.K_c:
					return
		pygame.display.update()
		clock.tick(fps)

def healthbar(phealth,ehealth):
	pcolor=green
	ecolor=green
	if phealth>=75:
		pcolor=green
	elif phealth>25:
		pcolor=yellow
	elif phealth<=25:
		pcolor=red
	if ehealth>=75:
		ecolor=green
	elif ehealth>25:
		ecolor=yellow
	elif ehealth<=25:
		ecolor=red

	pygame.draw.rect(gameDisplay,black,(638,28,104,34))
	pygame.draw.rect(gameDisplay,black,(118,28,104,34))
	pygame.draw.rect(gameDisplay,pcolor,(640,30,phealth,30))
	pygame.draw.rect(gameDisplay,ecolor,(120,30,ehealth,30))

def gameloop():
	gameOver=False
	gameExit=False
	tankx=int(screenWidth*0.9)
	tanky=int(screenHeight*0.9)
	etankX=int(screenWidth*0.1)
	etankY=int(screenHeight*0.9)
	playerhealth=100
	enemyhealth=100
	xloc=screenWidth/2+random.randint(-0.2*tankWidth,0.2*tankHeight)
	randomHeight=random.randrange(screenHeight*0.1,screenHeight*0.6)
	barrierwidth=50
	power=50
	damage=0
	pdamage=0
	powerchange=0
	turretpos=0
	eturretpos=0
	index=0
	movetank=0
	while not gameExit:
		while gameOver==True:
			gameDisplay.blit(gameoverim,(0,0))
			if playerhealth<enemyhealth:
				displaymsg("You Lose",red,ydisplace=-10,size="mid")
			else:
				displaymsg("You won",red,ydisplace=-10,size="mid")
			pointer_pos=pygame.mouse.get_pos()
			click=pygame.mouse.get_pressed()

			if 150+100 > pointer_pos[0] >150 and 500+50 > pointer_pos[1] >500:
				button("play",green,140,490,110,60)
				if click[0]==1:
					playerhealth=100
					enemyhealth=100
					tankx=int(screenWidth*0.9)
					tanky=int(screenHeight*0.9)
					etankX=int(screenWidth*0.1)
					etankY=int(screenHeight*0.9)
					gameOver=False
			else:
				button("play",lightergreen,150,500,100,50)

			if 550+100 > pointer_pos[0] >550 and 500+50 > pointer_pos[1] >500:
				button("quit",red,540,490,110,60,action="quit")
			else:
				button("quit",lightered,550,500,100,50)

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					pygame.quit()
					quit()
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_c:
						gameloop()
					if event.key==pygame.K_q:
						pygame.quit()
						quit()
			pygame.display.update()

		for event in pygame.event.get():
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					movetank-=5
				if event.key==pygame.K_RIGHT:
					movetank+=5
				if event.key==pygame.K_UP:
					index+=1
				if event.key==pygame.K_DOWN:
					index-=1
				if event.key==pygame.K_a:
					powerchange=1
				if event.key==pygame.K_d:
					powerchange=-1
				if event.key==pygame.K_p:
					pause()
				if event.key==pygame.K_SPACE:
					edamage=fireShell(gun,tankx,tanky,turretpos,power,xloc,randomHeight,barrierwidth,etankX,etankY)
					pdamage=efireShell(enemygun,etankX,etankY,8,60,xloc,randomHeight,barrierwidth,tankx,tanky)
					enemyhealth-=edamage
					playerhealth-=pdamage

					possiblemovements=['f','r']
					moveIndex=random.randrange(0,2)
					for x in range(10):
						if xloc>etankX:
							if possiblemovements[moveIndex]=='f':
								etankX+=5
							else:
								etankX-=5
						elif etankX<screenWidth:
							etankX+=5
						gameDisplay.blit(mainbg,(0,0))
						gun=tank(tankx,tanky,turretpos)
						enemygun=enemy_tank(etankX,etankY,eturretpos)
						barrier(xloc,randomHeight,barrierwidth)
						healthbar(playerhealth,enemyhealth)
						gameDisplay.blit(base,(0,screenHeight-ground))
						handlepower(power)
						pygame.display.update()
						clock.tick(fps)

			if event.type==pygame.KEYUP:
				if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
					movetank=0
				if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
					index=0
				if event.key==pygame.K_a or event.key==pygame.K_d:
					powerchange=0
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.blit(mainbg,(0,0))
		gun=tank(tankx,tanky,turretpos)
		enemygun=enemy_tank(etankX,etankY,eturretpos)
		barrier(xloc,randomHeight,barrierwidth)
		healthbar(playerhealth,enemyhealth)
		gameDisplay.blit(base,(0,screenHeight-ground))
		handlepower(power)

		if enemyhealth<1 or playerhealth<1:
			gameOver=True

		tankx+=movetank
		turretpos+=index
		if turretpos<0:
			turretpos=0
		elif turretpos>8:
			turretpos=8
		power+=powerchange
		if power>100:
			power=100
		if power<1:
			power=1

		if etankX>xloc-40:
			etankX-=5
		if xloc+50>tankx-tankWidth:
			tankx+=5
		if tankx+tankWidth>screenWidth:
			tankx-=5
		if etankX<1:
			etankX+=5

		pygame.display.update()
		clock.tick(fps)


intro()