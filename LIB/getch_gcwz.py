#This file is part of RogueBox Adventures.
#
#    RogueBox Adventures is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RogueBox Adventures is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RogueBox Adventures.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import time
import os
	
basic_path = os.path.dirname(os.path.realpath('getch.py')) #just get the execution path for resources
basic_path = basic_path.replace('/LIB','')
sfx_path = basic_path + os.sep + 'AUDIO' + os.sep + 'SFX' + os.sep
pygame.init()
clock = pygame.time.Clock()
sfxlist = {'wasd': pygame.mixer.Sound(sfx_path + 'wasd.ogg'), 'e' : pygame.mixer.Sound(sfx_path + 'e.ogg'), 'b' : pygame.mixer.Sound(sfx_path + 'b.ogg'), 'i' : pygame.mixer.Sound(sfx_path + 'i.ogg'), 'x' : pygame.mixer.Sound(sfx_path + 'x.ogg'), 'f' : pygame.mixer.Sound(sfx_path + 'f.ogg')}

key_name = {'e':'B','b':'A','x':'X','f':'SE','i':'ST','wasd':'D-PAD','ws':'D-PAD'}

def getch(x=640,y=360,sfx=0,mode=0,mouse=1):#x,y,mouse > /dev/null
	
	g = 'foo'
	run = 0
	
	while g == 'foo':
		clock.tick(30)
		run +=1
		for event in pygame.event.get():
							
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_UP:
					g='w'
					
				if event.key == pygame.K_LEFT:
					g='a'
					
				if event.key == pygame.K_DOWN:
					g='s'
					
				if event.key == pygame.K_RIGHT:
					g='d'
					
				if event.key == pygame.K_LALT: #e=a
					g='e'
					
				if event.key == pygame.K_LSHIFT: #x=x
					g='x'
				
				if event.key == pygame.K_LCTRL:  #b=b
					g='b'
				
				if event.key == pygame.K_RETURN: #start=i
					g='i'
					
				if event.key == pygame.K_ESCAPE: #select=f
					g='f'
					
				if sfx == 1:#in menus
					if event.key == pygame.K_TAB:
						g='a'
					if event.key == pygame.K_BACKSPACE:
						g='d'
					
		if run > 59:
			if mode == 1:
				g='none'
			run = 0
			
		if sfx == 1:
			if g == 'w' or g == 'a' or g == 's' or g == 'd':
				file_name = 'wasd'
			else:
				file_name = g
						
			if g != 'none' and g != 'foo':
				try:
					sfxlist[file_name].play(maxtime=1000)
				except:
					None
					
	return g
