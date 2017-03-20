#! /usr/bin/python
# -*- coding: utf-8 -*-

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

import datetime
import time
from time import sleep as sleep
import sys
import os

low_res = False
gcwz_input = False
home_save = False
force_small_worlds = False

Time_ready = False
entrance_x = 0
entrance_y = 0

basic_path = os.path.dirname(os.path.realpath('main.py')) #just get the execution path for resources

for t in sys.argv:
	
	if t == '-m':
		p = os.path.expanduser(basic_path)
		lf = open('rba.desktop','w')
		lf.write('[Desktop Entry]\n')
		lf.write('Type=Application\n')
		lf.write('Name=RogueBox Adventures\n')
		lf.write('Comment=A RogueBox Game\n')
		lf.write('Exec=sh ' + p + os.sep + 'LIB' + os.sep + 'run.sh\n')
		lf.write('Icon=' + p + os.sep + 'icon_big.png\n')
		lf.write('Terminal=false\n')
		lf.write('Categories=Game;')
		lf.close()
		
		rf_path = p + os.sep + 'LIB' + os.sep + 'run.sh'
		rf = open(rf_path,'w')
		rf.write('#This file was generated automatically. Please don\'t change anything.\n')
		rf.write('cd ' + p + '\n')
		rf.write('python ' + p + os.sep + 'main.py')
		
		sys_com = 'chmod +x ' + p + os.sep + 'rba.desktop'
		os.system(sys_com)
		exit(0)
	
	if t == '-l':
		low_res = True
		
	if t == '-g':
		gcwz_input = True
		
	if t == '-s':
		force_small_worlds = True
		
	if t == '-h':
		home_save = True
		
lib_path = basic_path + os.sep + 'LIB'
data_path = basic_path + os.sep + 'DATA'
if home_save == False:
	save_path = basic_path + os.sep + 'SAVE' + os.sep + 'World0'
else:
	save_path = os.path.expanduser('~') + os.sep + '.config' + os.sep + 'RogueBox-Adventures' + os.sep + 'SAVE' + os.sep + 'World0'
 
path = save_path.replace(os.sep+'World0','')
if os.path.exists(path) == False:
	for c in range(0,5):
		ph = path +  os.sep + 'World' + str(c)
		os.makedirs(ph)
del path

playing = False
sys.path.append(lib_path)
max_map_size = 52
monitor = [0,0]

try:
	import cPickle as p
except:
	import pickle as p
	
try:
	p.DEFAULT_PROTOCOL=0
except:
	p.HIGHEST_PROTOCOL=0

import random
if gcwz_input == True:
	from getch_gcwz import *
else:
	from getch import *
from tile import tile
from attribute import attribute
from item import *
from countdown import *
import pygame
from gra_files import *
from util import *
from monster import monster
from copy import deepcopy
from buffs import buffs
from itemlist import *
from tilelist import *
from monsterlist import *
from text import texts
from version import *

game_options = game_options(basic_path,home_save)

if game_options.check_version == 1:
	ver_string = check_version()
else:
	ver_string = ' '
		
class g_screen():
	
	def __init__(self, mode = game_options.screenmode, show_logo = True):
		
		string = 'RogueBoxAdventures ' + version
		pygame.display.set_caption(string)
		icon = pygame.image.load('icon_small.png')
		pygame.display.set_icon(icon)
		
		global monitor
		
		self.fire_mode = 0 #0: normal, 1: fire
		self.win_mode = mode
		self.hit_matrix = []
		
		for y in range(0,12):
			self.hit_matrix.append([])
			for  x in range(0,15):
				self.hit_matrix[y].append(0)
		
		pygame.init()
		
		display_info = pygame.display.Info()
		
		if monitor == [0,0]:
			monitor[0] = display_info.current_w
			monitor[1] = display_info.current_h
		
		self.displayx = monitor[0]
		self.displayy = monitor[1]
		
		
		#check if the screenmode is 16:9
		
		if float(self.displayx/self.displayy) < float(16/9):
			self.displayx = int((self.displayy*9)/16)
		elif float(self.displayx/self.displayy) > float(16/9):
			self.displayy = int((self.displayx*9)/16)
		
		winstyle = pygame.FULLSCREEN
		
		if self.win_mode == 2:  
			self.screen = pygame.display.set_mode((self.displayx,self.displayy),winstyle)
			pygame.mouse.set_visible(game_options.mousepad)		
		elif self.win_mode == 0 and low_res == False:
			self.screen = pygame.display.set_mode((640,360))
			self.displayx = 640
			self.displayy = 360
		elif self.win_mode == 1 and low_res == False:
			self.screen = pygame.display.set_mode((1280,720))
			self.displayx = 1280
			self.displayy = 720
		 
		if low_res == True:
			self.screen = pygame.display.set_mode((320,240))
			pygame.mouse.set_visible(False)
			self.displayx = 320
			self.displayy = 240
		
		font_path = basic_path + os.sep + 'FONT' + os.sep + 'PressStart2P.ttf'
		self.font = pygame.font.Font(font_path,8)
		
		if low_res == True:
			str_ext = '_low_res'
		else:
			str_ext = ''
		
		if show_logo == True:
			display_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep
			ran = random.randint(0,4)
			i_name = display_path + 'logo' + str(ran) + str_ext + '.png'
			i = pygame.image.load(i_name)
			i = pygame.transform.scale(i,(self.displayx,self.displayy))
			self.screen.blit(i,(0,0))
			pygame.display.flip()
			getch(640,360,mode=1)
			
			display_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep
			i_name = display_path + 'oga' + str_ext + '.png'
			i = pygame.image.load(i_name)
			i = pygame.transform.scale(i,(self.displayx,self.displayy))
			self.screen.blit(i,(0,0))
			pygame.display.flip()
			getch(640,360,mode=1)
	
	def reset_hit_matrix(self):
		
		self.hit_matrix = []
		
		for y in range(0,12):
			self.hit_matrix.append([])
			for  x in range(0,15):
				self.hit_matrix[y].append(0)
				
	def write_hit_matrix(self,x,y,style):
		
		#style: 0:nothing
		#		1:fire_path
		#		2:fire_path_monster
		#		3:miss
		#		4:hit
		#		5:critical
		#		6:heal
		#		7:teleport
		#		8:minus_gem
		#		9:plus_gem
		#		10:plus_fish
		#		11:plus_shoe
		#		12:monster_lvl_up
				
		xx = x - player.pos[0] + 7
		yy = y - player.pos[1] + 6
		
		try:
			self.hit_matrix[yy][xx] = style
		except:
			None
	
	def render_hits(self):
		
		s = pygame.Surface((480,360))
			
		s.fill((255,0,255))
		if low_res == False:
			start = 0
			plusx = 16
			plusy = -12
		else:
			start = 2
			plusx = -8
			plusy = -6
			
		
		for y in range(start,len(self.hit_matrix)):
			for x in range(start,len(self.hit_matrix[0])):
					
				if self.hit_matrix[y][x] == 1:
					s.blit(gra_files.gdic['display'][11],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 2:
					s.blit(gra_files.gdic['display'][12],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 3:
					s.blit(gra_files.gdic['display'][13],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 4:
					s.blit(gra_files.gdic['display'][14],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 5:
					s.blit(gra_files.gdic['display'][15],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 6:
					s.blit(gra_files.gdic['display'][23],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 7:
					s.blit(gra_files.gdic['display'][24],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 8:
					s.blit(gra_files.gdic['display'][26],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 9:
					s.blit(gra_files.gdic['display'][27],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 10:
					s.blit(gra_files.gdic['display'][42],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 11:
					s.blit(gra_files.gdic['display'][43],(((x-start)*32)+plusx,(y-start)*32+plusy))
				elif self.hit_matrix[y][x] == 12:
					s.blit(gra_files.gdic['display'][51],(((x-start)*32)+plusx,(y-start)*32+plusy))

		s.set_colorkey((255,0,255),pygame.RLEACCEL)	
		s = s.convert_alpha()
		return s
		
	def render_main_menu(self):
		
		if home_save == False:
			display_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep
			alt_path = display_path
		else:
			display_path = os.path.expanduser('~') + os.sep + '.config' + os.sep + 'RogueBox-Adventures' + os.sep
			alt_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep
	
		num = 0
		
		master_loop = True
		run = True
		
		while run:
			
			if low_res == False: 
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
		
			s.fill((48,48,48))
			try:
				i_name = display_path + 'tmp.png'
				i = pygame.image.load(i_name)
				i.set_colorkey((255,0,255),pygame.RLEACCEL)
				i = i.convert_alpha()
				s.blit(i,(0,0))
			except:
				i_name = alt_path + 'alt.png'
				i = pygame.image.load(i_name)
				i.set_colorkey((255,0,255),pygame.RLEACCEL)
				i = i.convert_alpha()
				s.blit(i,(0,0))
			
			if low_res == False:	
				s.blit(gra_files.gdic['display'][16],(0,0))
			else:	
				s.blit(gra_files.gdic['display'][22],(0,0))
			
			menu_list = ('PLAY','OPTIONS','CREDITS','QUIT')
			
			for c in range(0,len(menu_list)):
				name_image = self.font.render(menu_list[c],1,(0,0,0))
				if low_res ==False:
					s.blit(name_image,(210,145+(c*45)))
				else:
					s.blit(name_image,(125,50+(c*45)))
			if low_res == False:	
				s.blit(gra_files.gdic['display'][4],(185,138+(num*45)))
			else:
				s.blit(gra_files.gdic['display'][4],(100,43+(num*45)))
			
			if game_options.check_version == 1:
				
				if ver_string == 'This version is up to date.':
					ver_image = self.font.render(ver_string,1,(0,255,0))
				elif ver_string == 'Old version!!! Please update.':
					ver_image = self.font.render(ver_string,1,(255,0,0))
				else:
					ver_image = self.font.render(ver_string,1,(255,255,255))
				
				ver_image2 = self.font.render(ver_string,1,(0,0,0))
				
				if low_res == True:
					s.blit(ver_image2,(12,230))
					s.blit(ver_image,(10,230))
				else:
					s.blit(ver_image2,(12,340))
					s.blit(ver_image,(10,340))
			
			if game_options.mousepad == 0 and low_res == False:
				s_h = pygame.Surface((160,360))
				s_h.fill((48,48,48))
				s.blit(s_h,(480,0))
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			else:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			
			if low_res == False:
				s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
				master_loop = False
				run = False
			
			if ui == 'w':
				num -= 1
				if num < 0:
					num = 0
					
			elif ui == 's':
				num += 1
				if num > 3:
					num = 3
			
			elif ui == 'e':
				if num == 0:
					test = screen.choose_save_path()
					if test == 'exit':
						master_loop = False
					run = False
				elif num == 1:
					test = screen.render_options()
					if test == 'exit':
						master_loop = False
						run = False
				elif num == 2:
					test = screen.render_credits()
					if test == 'exit':
						master_loop = False
						run = False
				elif num == 3:
					master_loop = False
					run = False
		
		return master_loop
	
	def render_crash(self):
		
		run = True
		
		while run:
			self.screen.fill((48,48,48))
			string = []
			string.append('Sorry, something went wrong.')
			string.append('Check out debug.txt for more informations.')
			debug_location = '('+save_path+')'
			for c in range(0,6):
				debug_location = debug_location.replace('World'+str(c),'debug.txt')
			string.append(debug_location)
			st = []
			for i in string:
				st.append(self.font.render(i,1,(255,255,255)))
			for j in range(0,len(st)): 	
				self.screen.blit(st[j],(5,25+j*25))
		
			pygame.display.flip()
		
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
		
			if ui != 'none':
				run = False
		
	def choose_save_path(self):
		
		global save_path
		global playing
		global master_loop
		
		if home_save == True:
			path = os.path.expanduser('~') + os.sep + '.config' + os.sep + 'RogueBox-Adventures'
		else:
			path = basic_path
		
		run = True
		while run:
			
			menu_items = []
		
			for c in range(0,5):
				save_path = path + os.sep + 'SAVE' + os.sep + 'World' + str(c)
				p_attribute = attribute(2,2,2,2,2,10,10)
				p_inventory = inventory()
				player_help = player_class ('-EMPTY SLOT-', 'local_0_0', p_attribute,p_inventory, build= 'Auto')
				
				if player_help.name != '-EMPTY SLOT-':
					item_string = player_help.name + ' LVL:' + str(player_help.lvl)
				else:
					item_string = '-EMPTY SLOT-'
					
				menu_items.append(item_string)
				
			menu_items.append('~~ERASE~~')
			menu_items.append('~~BACK~~')
				
			choice = screen.get_choice('Choose a saved game',menu_items,False)
			if choice == 'exit':
				master_loop = False
				run = False
				return('exit')
			
			if choice < 5:
				save_path = path + os.sep + 'SAVE' + os.sep + 'World' + str(choice)
				playing = True
				run = False
				
			elif choice == 5:
				menu_items_erase = []
				
				for d in range(0,5):
					menu_items_erase.append(menu_items[d])
				
				menu_items_erase.append('~~BACK~~')
					
				choice2 = screen.get_choice('Choose a game to erase',menu_items_erase,False,'Warning')
				
				if choice2 < 5:
						
					save_path = path + os.sep + 'SAVE' + os.sep + 'World' + str(choice2)
						
					try:	
						
						choice3 = screen.get_choice('Are you sure?',('No','Yes'),False,'Warning')
						
						if choice3 == 1:
							h = ('world.data','time.data','player.data','gods.data')
							
							for i in h:	
								p = save_path + os.sep + i
								os.remove(p)
					except:
						None
						
			elif choice == 6:
				run = False
	
	def save_tmp_png(self):
		
		x = player.pos[0]
		if x-10 < 0:
			x += -1*(x-11)
		elif x+10 > max_map_size-2:
			x -= 10
			
		y = player.pos[1]
		if y-10 < 0:
			y += -1*(y-11)
		elif y+10 > max_map_size-2:
			y -= 10
			
		z =  player.pos[2]
		
		s = pygame.Surface((480,360))
		
		for yy in range(-5,10):
			for xx in range(-7,8):
				
				  
				t_pos = world.maplist[z][player.on_map].tilemap[y+yy][x+xx].tile_pos
				t_replace = world.maplist[z][player.on_map].tilemap[y+yy][x+xx].replace
					
				if t_replace == None:
					s.blit(gra_files.gdic['tile32'][t_pos[1]][t_pos[0]],((xx+7)*32,(yy+5)*32))
				else:
					try:
						#render the replaced tile under the replacing one. eg.: for stacks
						s.blit(gra_files.gdic['tile32'][t_replace.tile_pos[1]][t_replace.tile_pos[0]],((xx+7)*32,(yy+5)*32))
						s.blit(gra_files.gdic['tile32'][t_pos[1]][t_pos[0]],((xx+7)*32,(yy+5)*32))
					except:
						None
		
		if home_save == False:
			tmp_save_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep + 'tmp.png'
		else:
			tmp_save_path = os.path.expanduser('~') + os.sep + '.config' + os.sep + 'RogueBox-Adventures' + os.sep + 'tmp.png'
					
		pygame.image.save(s,tmp_save_path)
							
	
	def re_init(self): # For changing screenmode
		
		options_path = save_path.replace(os.sep + 'World0','')
		
		mode = game_options.screenmode
		
		if self.win_mode < 2:
			mode += 1
		else:
			mode = 0
		game_options.screenmode = mode
		save_options(game_options,options_path,os.sep)
		
		self.__init__(game_options.screenmode,False)
	
	def generate_light_effect(self):
		
		if player.pos[2] > 0:
			y = 1
		else:
			y= 0
			
		x = time.hour
		
		if player.pos[2] == 0:
			if time.hour == 12:
				alpha = 0
			elif time.hour < 12:
				alpha = 60-(time.hour*5)
			elif time.hour > 12:
				alpha = 0+((time.hour-12)*5)
		else:
			alpha = 135
			
		light_color = gra_files.gdic['lightmap'].get_at((x,y))
		
		if low_res == False:
			s = pygame.Surface((640,360))
		else:
			s = pygame.Surface((320,240))
			
		s.fill(light_color)
		
		if player.buffs.light > 0:
			if low_res == False:
				pygame.draw.circle(s,(255,0,255),[254,197],120,0)
			else:
				pygame.draw.circle(s,(255,0,255),[169,140],60,0)
				
			s.set_colorkey((255,0,255),pygame.RLEACCEL)
		
		s.set_alpha(alpha)
	
		return s
		
	def render(self,mes_num, simulate = False):
		
		radius = 6
		
		if player.pos[2] > 0:
			radius = 2
		elif player.pos[2] == 0:
			if time.hour > 22 or time.hour < 4:
				radius = 2 
			elif time.hour > 21 or time.hour < 5:
				radius = 3 
			elif time.hour > 20 or time.hour < 6:
				radius = 4 
			elif time.hour > 19 or time.hour < 7:
				radius = 5 
			
		if player.buffs.light > 0:
			radius = 6
			
		if player.buffs.blind > 0:
			radius = 0 
		
		s = pygame.Surface((640,360))
		
		test = message.sget()
		
		s.fill((48,48,48)) #paint it grey(to clear the screen)
		
		if low_res == False:
			start_pos_x = 240 #the center of the main map view
			start_pos_y = 180
		else:
			start_pos_x = 152 #the center of the main map view
			start_pos_y = 122
		
		ymin = player.pos[1]-6
		if ymin < 0:
			ymin = 0		
		ymax = player.pos[1]+7
		xmin = player.pos[0]-8
		if xmin < 0: 
			xmin = 0
		xmax = player.pos[0]+8
		
		for y in range(ymin,ymax):
			for x in range(xmin,xmax):
								
				rx = x-player.pos[0]
				ry = y-player.pos[1]
				
				distance = ((rx)**2+(ry)**2)**0.5
				
				try:
								
					t_pos = world.maplist[player.pos[2]][player.on_map].tilemap[y][x].tile_pos
					t_known = world.maplist[player.pos[2]][player.on_map].known[y][x]
					t_replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace
						
					if t_known == 1:
						if t_replace == None:
							s.blit(gra_files.gdic['tile32'][t_pos[1]][t_pos[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
						else:
							#render the replaced tile under the replacing one. eg.: for stacks
							s.blit(gra_files.gdic['tile32'][t_replace.tile_pos[1]][t_replace.tile_pos[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
							s.blit(gra_files.gdic['tile32'][t_pos[1]][t_pos[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
							
						
						s.blit(gra_files.gdic['display'][6],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
					
						if world.maplist[player.pos[2]][player.on_map].npcs[y][x] != 0:	
							ran = random.randint(0,1)
							if world.maplist[player.pos[2]][player.on_map].npcs[y][x].techID == ml.mlist['special'][0].techID or world.maplist[player.pos[2]][player.on_map].npcs[y][x].techID == ml.mlist['special'][1].techID or world.maplist[player.pos[2]][player.on_map].npcs[y][x].techID == ml.mlist['special'][3].techID:
								#if this is a vase, a monster vase or a sleepng mimic show them like they would be tile ojects
								sprite_pos = world.maplist[player.pos[2]][player.on_map].npcs[y][x].sprite_pos
								s.blit(gra_files.gdic['monster'][sprite_pos[1]][sprite_pos[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
								ran = 0
						
							if ran == 1:
								s.blit(gra_files.gdic['display'][7],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
							else:
								s.blit(gra_files.gdic['display'][6],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
						if low_res == False:
							if round(distance) <= radius+1 or round(distance) >= radius-1:
							
								run = True
								c = 0
							
								while run:
								
									try:
										yy = ((ry*c)/distance)
									except:
										yy = 1
						
									try:
										xx = ((rx*c)/distance)
									except:
										xx = 1
								
									view_x = int(xx) + player.pos[0]
									view_y = int(yy) + player.pos[1]
								
									t_pos = world.maplist[player.pos[2]][player.on_map].tilemap[view_y][view_x].tile_pos
									t_known = world.maplist[player.pos[2]][player.on_map].known[view_y][view_x]
									t_replace = world.maplist[player.pos[2]][player.on_map].tilemap[view_y][view_x].replace	
								
									if t_known == 1:
										if t_replace == None:
											s.blit(gra_files.gdic['tile32'][t_pos[1]][t_pos[0]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
										else:
											#render the replaced tile under the replacing one. eg.: for stacks
											s.blit(gra_files.gdic['tile32'][t_replace.tile_pos[1]][t_replace.tile_pos[0]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
											s.blit(gra_files.gdic['tile32'][t_pos[1]][t_pos[0]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
							
										if world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x] != 0:#render monsters
											pos = world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x].sprite_pos
											s.blit(gra_files.gdic['monster'][pos[1]][pos[0]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
											if world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x].move_border > 9:
												None
											elif world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x].AI_style == 'ignore':
												s.blit(gra_files.gdic['display'][28],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
												lvl = str(world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x].lvl)
												if len(lvl) == 1:
													lvl = '0'+lvl
												elif len(lvl) > 2:
													lvl = lvl[0]+'+'
												s.blit(gra_files.gdic['num'][lvl[0]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)+6))	
												s.blit(gra_files.gdic['num'][lvl[1]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)+14))
											elif world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x].AI_style == 'flee':
												s.blit(gra_files.gdic['display'][29],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
												lvl = str(world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x].lvl)
												if len(lvl) == 1:
													lvl = '0'+lvl
												elif len(lvl) > 2:
													lvl = lvl[0]+'+'
												s.blit(gra_files.gdic['num'][lvl[0]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)+6))	
												s.blit(gra_files.gdic['num'][lvl[1]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)+14))
											elif world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x].AI_style == 'hostile':
												s.blit(gra_files.gdic['display'][30],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
												lvl = str(world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x].lvl)
												if len(lvl) == 1:
													lvl = '0'+lvl
												elif len(lvl) > 2:
													lvl = lvl[0]+'+'
												s.blit(gra_files.gdic['num'][lvl[0]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)+6))	
												s.blit(gra_files.gdic['num'][lvl[1]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)+14))
											else:
												None
								
										if view_x == player.pos[0] and view_y == player.pos[1]:
											player_pos_help = (view_x,view_y)
											if player.inventory.wearing['Background'] != player.inventory.nothing:
												s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Background'].gra_pos[player.gender][0]][player.inventory.wearing['Background'].gra_pos[player.gender][1]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
												
											skinstring = 'SKIN_' + player.gender + '_' + str(player.style +1)
											s.blit(gra_files.gdic['char'][skinstring],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
											
											try:
												render_hair = (player.inventory.wearing['Hat'].override_hair == False)
											except:
												render_hair = True
											
											if player.inventory.wearing['Head'] == player.inventory.nothing and render_hair:  
												hairstring = 'HAIR_' + player.gender + '_' + str(player.style +1)
												s.blit(gra_files.gdic['char'][hairstring],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
												if player.inventory.wearing['Hat'] != player.inventory.nothing:
													s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Hat'].gra_pos[player.gender][0]][player.inventory.wearing['Hat'].gra_pos[player.gender][1]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
												
											else:
												if player.inventory.wearing['Hat'] == player.inventory.nothing:
													helmetstring = player.gender + '_' + player.inventory.wearing['Head'].material + '_' + player.inventory.wearing['Head'].classe
													s.blit(gra_files.gdic['char'][helmetstring],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
												else:
													if render_hair == True:
														hairstring = 'HAIR_' + player.gender + '_' + str(player.style +1)
														s.blit(gra_files.gdic['char'][hairstring],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
													s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Hat'].gra_pos[player.gender][0]][player.inventory.wearing['Hat'].gra_pos[player.gender][1]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
														
											if player.inventory.wearing['Clothing'] == player.inventory.nothing:
												if player.inventory.wearing['Body'] != player.inventory.nothing:
													armorstring = player.gender + '_' + player.inventory.wearing['Body'].material + '_' + player.inventory.wearing['Body'].classe
													s.blit(gra_files.gdic['char'][armorstring],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
									
												if player.inventory.wearing['Legs'] != player.inventory.nothing:
													cuissestring = player.gender + '_' + player.inventory.wearing['Legs'].material + '_' + player.inventory.wearing['Legs'].classe
													s.blit(gra_files.gdic['char'][cuissestring],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
								
												if player.inventory.wearing['Feet'] != player.inventory.nothing:
													shoestring = player.gender + '_' + player.inventory.wearing['Feet'].material + '_' + player.inventory.wearing['Feet'].classe
													s.blit(gra_files.gdic['char'][shoestring],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))

											else:
												s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Clothing'].gra_pos[player.gender][0]][player.inventory.wearing['Clothing'].gra_pos[player.gender][1]],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
						
											if player.inventory.wearing['Hold(R)'] != player.inventory.nothing:
												weaponstring = 'WEAPONS_' + player.inventory.wearing['Hold(R)'].material + '_' + player.inventory.wearing['Hold(R)'].classe
												s.blit(gra_files.gdic['char'][weaponstring],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))
											
											
											if player.inventory.wearing['Hold(L)'] != player.inventory.nothing:
												weaponstring = 'WEAPONS_' + player.inventory.wearing['Hold(L)'].material + '_' + player.inventory.wearing['Hold(L)'].classe
												s.blit(gra_files.gdic['char'][weaponstring],(start_pos_x+((view_x-player.pos[0])*32),start_pos_y+((view_y-player.pos[1])*32)))					
										
									if c >= radius or world.maplist[player.pos[2]][player.on_map].tilemap[view_y][view_x].transparency == False:
										run = False
									else:
										c+=1
						
						elif low_res == True:
							
							if round(distance) <= radius:
								if t_replace == None:
									s.blit(gra_files.gdic['tile32'][t_pos[1]][t_pos[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
								else:
									#render the replaced tile under the replacing one. eg.: for stacks
									s.blit(gra_files.gdic['tile32'][t_replace.tile_pos[1]][t_replace.tile_pos[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
									s.blit(gra_files.gdic['tile32'][t_pos[1]][t_pos[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
								
								if world.maplist[player.pos[2]][player.on_map].npcs[y][x] != 0:#render monsters
											pos = world.maplist[player.pos[2]][player.on_map].npcs[y][x].sprite_pos
											s.blit(gra_files.gdic['monster'][pos[1]][pos[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
											if world.maplist[player.pos[2]][player.on_map].npcs[y][x].move_border > 9:
												None
											elif world.maplist[player.pos[2]][player.on_map].npcs[y][x].AI_style == 'ignore':
												s.blit(gra_files.gdic['display'][28],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
												lvl = str(world.maplist[player.pos[2]][player.on_map].npcs[y][x].lvl)
												if len(lvl) == 1:
													lvl = '0'+lvl
												elif len(lvl) > 2:
													lvl = lvl[0]+'+'
												s.blit(gra_files.gdic['num'][lvl[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)+6))	
												s.blit(gra_files.gdic['num'][lvl[1]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)+14))
											elif world.maplist[player.pos[2]][player.on_map].npcs[view_y][view_x].AI_style == 'flee':
												s.blit(gra_files.gdic['display'][29],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
												lvl = str(world.maplist[player.pos[2]][player.on_map].npcs[y][x].lvl)
												if len(lvl) == 1:
													lvl = '0'+lvl
												elif len(lvl) > 2:
													lvl = lvl[0]+'+'
												s.blit(gra_files.gdic['num'][lvl[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)+6))	
												s.blit(gra_files.gdic['num'][lvl[1]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)+14))
											elif world.maplist[player.pos[2]][player.on_map].npcs[y][x].AI_style == 'hostile':
												s.blit(gra_files.gdic['display'][30],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
												lvl = str(world.maplist[player.pos[2]][player.on_map].npcs[y][x].lvl)
												if len(lvl) == 1:
													lvl = '0'+lvl
												elif len(lvl) > 2:
													lvl = lvl[0]+'+'
												s.blit(gra_files.gdic['num'][lvl[0]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)+6))	
												s.blit(gra_files.gdic['num'][lvl[1]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)+14))
											else:
												None
												
								if x == player.pos[0] and y == player.pos[1]:
											player_pos_help = (x,y)
											if player.inventory.wearing['Background'] != player.inventory.nothing:
												s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Background'].gra_pos[player.gender][0]][player.inventory.wearing['Background'].gra_pos[player.gender][1]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
												
											skinstring = 'SKIN_' + player.gender + '_' + str(player.style +1)
											s.blit(gra_files.gdic['char'][skinstring],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
											
											try:
												render_hair = (player.inventory.wearing['Hat'].override_hair == False)
											except:
												render_hair = True
											
											if player.inventory.wearing['Head'] == player.inventory.nothing and render_hair:  
												hairstring = 'HAIR_' + player.gender + '_' + str(player.style +1)
												s.blit(gra_files.gdic['char'][hairstring],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
												if player.inventory.wearing['Hat'] != player.inventory.nothing:
													s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Hat'].gra_pos[player.gender][0]][player.inventory.wearing['Hat'].gra_pos[player.gender][1]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
												
											else:
												if player.inventory.wearing['Hat'] == player.inventory.nothing:
													helmetstring = player.gender + '_' + player.inventory.wearing['Head'].material + '_' + player.inventory.wearing['Head'].classe
													s.blit(gra_files.gdic['char'][helmetstring],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
												else:
													if render_hair == True:
														hairstring = 'HAIR_' + player.gender + '_' + str(player.style +1)
														s.blit(gra_files.gdic['char'][hairstring],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
													s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Hat'].gra_pos[player.gender][0]][player.inventory.wearing['Hat'].gra_pos[player.gender][1]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
														
											if player.inventory.wearing['Clothing'] == player.inventory.nothing:
												if player.inventory.wearing['Body'] != player.inventory.nothing:
													armorstring = player.gender + '_' + player.inventory.wearing['Body'].material + '_' + player.inventory.wearing['Body'].classe
													s.blit(gra_files.gdic['char'][armorstring],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
									
												if player.inventory.wearing['Legs'] != player.inventory.nothing:
													cuissestring = player.gender + '_' + player.inventory.wearing['Legs'].material + '_' + player.inventory.wearing['Legs'].classe
													s.blit(gra_files.gdic['char'][cuissestring],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
								
												if player.inventory.wearing['Feet'] != player.inventory.nothing:
													shoestring = player.gender + '_' + player.inventory.wearing['Feet'].material + '_' + player.inventory.wearing['Feet'].classe
													s.blit(gra_files.gdic['char'][shoestring],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))

											else:
												s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Clothing'].gra_pos[player.gender][0]][player.inventory.wearing['Clothing'].gra_pos[player.gender][1]],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
						
											if player.inventory.wearing['Hold(R)'] != player.inventory.nothing:
												weaponstring = 'WEAPONS_' + player.inventory.wearing['Hold(R)'].material + '_' + player.inventory.wearing['Hold(R)'].classe
												s.blit(gra_files.gdic['char'][weaponstring],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
											
											
											if player.inventory.wearing['Hold(L)'] != player.inventory.nothing:
												weaponstring = 'WEAPONS_' + player.inventory.wearing['Hold(L)'].material + '_' + player.inventory.wearing['Hold(L)'].classe
												s.blit(gra_files.gdic['char'][weaponstring],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
						
					elif t_known == 0:
						s.blit(gra_files.gdic['tile32'][0][3],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
					else:
						s.blit(gra_files.gdic['tile32'][0][3],(start_pos_x+((x-player.pos[0])*32),start_pos_y+((y-player.pos[1])*32)))
					
				except:
					None
		
		s.blit(screen.generate_light_effect(),(0,0))
		
		s.blit(self.render_hits(),(0,0))
		
		if self.fire_mode == 0:
			if (player.lp*100)/player.attribute.max_lp>20 and (player.attribute.hunger*100)/player.attribute.hunger_max>10 and (player.attribute.thirst*100)/player.attribute.thirst_max>10 and (player.attribute.tiredness*100)/player.attribute.tiredness_max>10:
				s.blit(gra_files.gdic['display'][0],(0,0)) #render gui
			else:
				s.blit(gra_files.gdic['display'][25],(0,0)) #render gui_warning
		else:
			s.blit(gra_files.gdic['display'][10],(0,0))
			s.blit(gra_files.gdic['display'][41],(start_pos_x+((player_pos_help[0]-player.pos[0])*32)-32,start_pos_y+((player_pos_help[1]-player.pos[1])*32)-32))
		
		#render tool info
			#1. Axe
		if player.inventory.wearing['Axe'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][44],(0,39))
		else:
			s.blit(gra_files.gdic['display'][46],(0,39))
			axestring = 'WEAPONS_' + player.inventory.wearing['Axe'].material + '_' + player.inventory.wearing['Axe'].classe
			s.blit(gra_files.gdic['char'][axestring],(0,39))
			s.blit(gra_files.gdic['display'][47],(0,39))
			axe_state = (15*player.inventory.wearing['Axe'].state)/100
			help_sur = pygame.Surface((axe_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(10,67))
			
			#2. Pickaxe
		if player.inventory.wearing['Pickaxe'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][45],(16,39))
		else:
			s.blit(gra_files.gdic['display'][46],(16,39))
			pickaxestring = 'WEAPONS_' + player.inventory.wearing['Pickaxe'].material + '_' + player.inventory.wearing['Pickaxe'].classe
			s.blit(gra_files.gdic['char'][pickaxestring],(16,39))
			s.blit(gra_files.gdic['display'][47],(16,39))
			pickaxe_state = (15*player.inventory.wearing['Pickaxe'].state)/100
			help_sur = pygame.Surface((pickaxe_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(26,67))
			
			#3. Melee weapon
		if player.inventory.wearing['Hold(R)'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][52],(32,39))
		else:
			s.blit(gra_files.gdic['display'][46],(32,39))
			melee_string = 'WEAPONS_' + player.inventory.wearing['Hold(R)'].material + '_' + player.inventory.wearing['Hold(R)'].classe
			if player.inventory.wearing['Hold(R)'].classe != 'spear':
				s.blit(gra_files.gdic['char'][melee_string],(32,39))
			else:
				h_sur = pygame.Surface((32,19))
				h_sur.fill((255,0,255))
				h_sur.blit(gra_files.gdic['char'][melee_string],(0,0))
				h_sur.set_colorkey((255,0,255),pygame.RLEACCEL)
				h_sur = h_sur.convert_alpha()
				s.blit(h_sur,(39,48))	
			s.blit(gra_files.gdic['display'][47],(32,39))
			melee_state = (15*player.inventory.wearing['Hold(R)'].state)/100
			help_sur = pygame.Surface((melee_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(42,67))
			
			#4. Magic weapon
		if player.inventory.wearing['Hold(L)'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][53],(48,39))
		else:
			s.blit(gra_files.gdic['display'][46],(48,39))
			magic_string = 'WEAPONS_' + player.inventory.wearing['Hold(L)'].material + '_' + player.inventory.wearing['Hold(L)'].classe
			if player.inventory.wearing['Hold(R)'].classe != 'runestaff':
				s.blit(gra_files.gdic['char'][magic_string],(42,39))
			else:
				h_sur = pygame.Surface((32,19))
				h_sur.fill((255,0,255))
				h_sur.blit(gra_files.gdic['char'][magic_string],(0,0))
				h_sur.set_colorkey((255,0,255),pygame.RLEACCEL)
				h_sur = h_sur.convert_alpha()
				s.blit(h_sur,(37,48))	
			s.blit(gra_files.gdic['display'][47],(48,39))
			magic_state = (15*player.inventory.wearing['Hold(L)'].state)/100
			help_sur = pygame.Surface((magic_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(58,67))
			
			#5. Necklace
		if player.inventory.wearing['Neck'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][40],(64,39))
		else:
			s.blit(gra_files.gdic['display'][46],(64,39))
			necklacestring = 'WEAPONS_' + player.inventory.wearing['Neck'].material + '_' + player.inventory.wearing['Neck'].classe
			s.blit(gra_files.gdic['char'][necklacestring],(64,39))
			s.blit(gra_files.gdic['display'][47],(64,39))
			necklace_state = (15*player.inventory.wearing['Neck'].state)/100
			help_sur = pygame.Surface((necklace_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(74,67))
		
			#6. Helmet
		if player.inventory.wearing['Head'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][54],(0,54))
		else:
			s.blit(gra_files.gdic['display'][46],(0,54))
			helmet_string = player.gender + '_' + player.inventory.wearing['Head'].material + '_' + player.inventory.wearing['Head'].classe
			h_sur = pygame.Surface((32,32))
			h_sur.fill((255,0,255))
			h_sur.blit(gra_files.gdic['char'][helmet_string],(0,0))
			pygame.draw.rect(h_sur,(255,0,255),(0,0,10,32),0)
			pygame.draw.rect(h_sur,(255,0,255),(0,0,32,4),0)
			pygame.draw.rect(h_sur,(255,0,255),(25,0,7,32),0)
			h_sur.set_colorkey((255,0,255),pygame.RLEACCEL)
			h_sur = h_sur.convert_alpha()
			s.blit(h_sur,(0,65))	
			s.blit(gra_files.gdic['display'][47],(0,54))
			helmet_state = (15*player.inventory.wearing['Head'].state)/100
			help_sur = pygame.Surface((helmet_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(10,82))
		
			#7. Armor
		if player.inventory.wearing['Body'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][55],(16,54))
		else:
			s.blit(gra_files.gdic['display'][46],(16,54))
			armor_string = player.gender + '_' + player.inventory.wearing['Body'].material + '_' + player.inventory.wearing['Body'].classe
			h_sur = pygame.Surface((32,32))
			h_sur.fill((255,0,255))
			h_sur.blit(gra_files.gdic['char'][armor_string],(0,0))
			pygame.draw.rect(h_sur,(255,0,255),(0,0,10,32),0)
			pygame.draw.rect(h_sur,(255,0,255),(25,0,7,32),0)
			h_sur.set_colorkey((255,0,255),pygame.RLEACCEL)
			h_sur = h_sur.convert_alpha()
			s.blit(h_sur,(16,55))	
			s.blit(gra_files.gdic['display'][47],(16,54))
			armor_state = (15*player.inventory.wearing['Body'].state)/100
			help_sur = pygame.Surface((armor_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(26,82))
			
			#8. Cuisse
		if player.inventory.wearing['Legs'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][56],(32,54))
		else:
			s.blit(gra_files.gdic['display'][46],(32,54))
			cuisse_string = player.gender + '_' + player.inventory.wearing['Legs'].material + '_' + player.inventory.wearing['Legs'].classe
			s.blit(gra_files.gdic['char'][cuisse_string],(32,50))	
			s.blit(gra_files.gdic['display'][47],(32,54))
			cuisse_state = (15*player.inventory.wearing['Legs'].state)/100
			help_sur = pygame.Surface((cuisse_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(42,82))
		
			#9. Shoes
		if player.inventory.wearing['Feet'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][57],(48,54))
		else:
			s.blit(gra_files.gdic['display'][46],(48,54))
			shoes_string = player.gender + '_' + player.inventory.wearing['Feet'].material + '_' + player.inventory.wearing['Feet'].classe
			s.blit(gra_files.gdic['char'][shoes_string],(49,46))	
			s.blit(gra_files.gdic['display'][47],(48,54))
			shoes_state = (15*player.inventory.wearing['Feet'].state)/100
			help_sur = pygame.Surface((shoes_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(58,82))	
		
			#10. Ring
		if player.inventory.wearing['Hand'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][39],(64,54))
		else:
			s.blit(gra_files.gdic['display'][46],(64,54))
			ring_string = 'WEAPONS_' + player.inventory.wearing['Hand'].material + '_' + player.inventory.wearing['Hand'].classe
			s.blit(gra_files.gdic['char'][ring_string],(64,54))
			s.blit(gra_files.gdic['display'][47],(64,54))
			ring_state = (15*player.inventory.wearing['Hand'].state)/100
			help_sur = pygame.Surface((ring_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(74,82))
			
		#render icons
			#1. Use
		if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].use_group == 'None' and world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] == 0:
			s.blit(gra_files.gdic['display'][32],(0,161))
			s.blit(gra_files.gdic['display'][34],(0,161))
		else:
			s.blit(gra_files.gdic['display'][31],(0,161))
			s.blit(gra_files.gdic['display'][33],(0,161))
			use_string = '['+key_name['e']+']action'
			use_image1 = self.font.render(use_string,1,(0,0,0))
			use_image2 = self.font.render(use_string,1,(255,255,255))
			s.blit(use_image1,(36,173))
			s.blit(use_image2,(34,173))
			
			#2. Fire
		if player.inventory.wearing['Hold(L)'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][32],(0,129))
			s.blit(gra_files.gdic['display'][36],(0,129))
		else:
			s.blit(gra_files.gdic['display'][31],(0,129))
			s.blit(gra_files.gdic['display'][35],(0,129))
			if self.fire_mode == False:
				fire_string = '['+key_name['f']+']fire'
			else:
				fire_string = '['+key_name['x']+']cancel'
			fire_image1 = self.font.render(fire_string,1,(0,0,0))
			fire_image2 = self.font.render(fire_string,1,(255,255,255))
			s.blit(fire_image1,(36,141))
			s.blit(fire_image2,(34,141))
		
			#3.Inventory
		#inventory_broken = False
		#for t in player.inventory.wearing:
		#	if player.inventory.wearing[t].state < 11 and player.inventory.wearing[t] != player.inventory.nothing:
		#		inventory_broken = True
		
		#if inventory_broken == False:
		#	s.blit(gra_files.gdic['display'][32],(0,97))
		#	s.blit(gra_files.gdic['display'][40],(0,97))
		#	inventory_string = '['+key_name['i']+']inventory'
		#	inventory_image1 = self.font.render(inventory_string,1,(0,0,0))
		#	inventory_image2 = self.font.render(inventory_string,1,(255,255,255))
		#else:
		#	s.blit(gra_files.gdic['display'][31],(0,97))
		#	s.blit(gra_files.gdic['display'][39],(0,97))
		#	inventory_string = '['+key_name['i']+']inventory!'
		#	inventory_image1 = self.font.render(inventory_string,1,(0,0,0))
		#	inventory_image2 = self.font.render(inventory_string,1,(255,0,0))
		
		#s.blit(inventory_image1,(36,109))
		#s.blit(inventory_image2,(34,109))
		
			#4.Focus
		s.blit(gra_files.gdic['display'][32],(0,97))#65
		try:
			focus_state = (32*player.mp/player.attribute.max_mp)
		except:
			focus_state = 1
		
		help_sur = pygame.Surface((focus_state,32))
		help_sur.fill((255,0,255))
		help_sur.blit(gra_files.gdic['display'][31],(0,0))
		help_sur.set_colorkey((255,0,255),pygame.RLEACCEL)
		help_sur = help_sur.convert_alpha()
		s.blit(help_sur,(0,97))
		
		if player.mp < player.attribute.max_mp:
			s.blit(gra_files.gdic['display'][38],(0,97))
			focus_string = 'unfocused'
		else:
			s.blit(gra_files.gdic['display'][37],(0,97))
			focus_string = 'focused'
			
		focus_image1 = self.font.render(focus_string,1,(0,0,0))
		focus_image2 = self.font.render(focus_string,1,(255,255,255))
		s.blit(focus_image1,(36,109))#77
		s.blit(focus_image2,(34,109))
		
		# render messages
		
		if low_res == False:
			mes_pos_y = 335
		else:
			mes_pos_y = 225
		
		mlist = test
		
		for c in range(0,5):
			shadow_image = self.font.render(mlist[c],1,(0,0,0))
			text_image = self.font.render(mlist[c],1,(255,255,255))
			s.blit(shadow_image,(2,mes_pos_y-(c*10)))
			s.blit(text_image,(0,mes_pos_y-(c*10)))
		
		#render lvl info
		
		lvl_string = str(player.lvl)
		if len(lvl_string) == 1:
			lvl_string = '0'+lvl_string
		lvl_image = self.font.render(lvl_string,1,(255,255,255))
		s.blit(lvl_image,(153,48))
		
		bar_length = 1 + ((319/100)*player.xp)
		xp_surface = pygame.Surface((bar_length,64))
		xp_surface.fill((255,0,255))
		xp_surface.blit(gra_files.gdic['display'][19],(0,0))
		xp_surface.set_colorkey((255,0,255),pygame.RLEACCEL)	
		xp_surface = xp_surface.convert_alpha()
		s.blit(xp_surface,(0,0))
		
		if game_options.mousepad == 1:
			if self.fire_mode == 0:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s.blit(gra_files.gdic['display'][9],(480,0))
		else:
			s_help = pygame.Surface((160,360))
			s_help.fill((48,48,48))
			s.blit(s_help,(480,0))
		
		#render buffs
		
		buffs = player.buffs.sget()
		if low_res == False:
			posx = 388 
			posy = 10
		else:
			posx = 228
			posy = 75
		
		for i in buffs:
			if i != ' ':
				buff_shadow = self.font.render(i,1,(0,0,0))
				s.blit(buff_shadow,(posx+2,posy))
				buff_image = self.font.render(i,1,(200,200,200))
				s.blit(buff_image,(posx,posy))
			else:
				None
				
			posy += 20
		
		
		#render date
		
		date_string = time.sget()
		posx = 235
		posy = 10
		
		date_image = self.font.render(date_string[0],1,(0,0,0))
		s.blit(date_image,(posx,posy))
		posy = 20
		time_image = self.font.render(date_string[1],1,(0,0,0))
		s.blit(time_image,(posx,posy))
		
		#render player info
			#lp
		lp_string = str(player.lp) + '/' + str(player.attribute.max_lp)
			
		posx = 13
		posy = 12
		
		if player.lp < 4: 
			lp_image = self.font.render(lp_string,1,(200,0,0))
		else:
			lp_image = self.font.render(lp_string,1,(0,0,0))
		s.blit(lp_image,(posx,posy))
			
			#hunger
		
		hunger_percent = int((100 * player.attribute.hunger) / player.attribute.hunger_max)
		
		hunger_string = str(hunger_percent) + '%'
		
		posx = 75
		posy = 12
		if hunger_percent < 11:
			hunger_image = self.font.render(hunger_string,1,(200,0,0))
		else:
			hunger_image = self.font.render(hunger_string,1,(0,0,0))
		s.blit(hunger_image,(posx,posy))
		
			#trirst
			
		thirst_percent = int((100 * player.attribute.thirst) / player.attribute.thirst_max)
		
		thirst_string = str(thirst_percent) + '%'
		
		posx = 125
		posy = 12
		
		if thirst_percent < 11:
			thirst_image = self.font.render(thirst_string,1,(200,0,0))
		else:
			thirst_image = self.font.render(thirst_string,1,(0,0,0))
		s.blit(thirst_image,(posx,posy))
		
			#tiredness
			
		tiredness_percent = int((100 * player.attribute.tiredness) / player.attribute.tiredness_max)
		
		tiredness_string = str(tiredness_percent) + '%'
		
		posx = 180
		posy = 12
		if tiredness_percent < 11:
			tiredness_image = self.font.render(tiredness_string,1,(200,0,0))
		else:
			tiredness_image = self.font.render(tiredness_string,1,(0,0,0))
		s.blit(tiredness_image,(posx,posy))
		
		if game_options.mousepad == 0 and low_res == False:
			s_help = pygame.Surface((640,360))
			s_help.fill((48,48,48))
			s_help.blit(s,(80,0))
			s = s_help		
		if low_res == False:
			s = pygame.transform.scale(s,(self.displayx,self.displayy))
		
		self.screen.blit(s,(0,0))
		
		if simulate == False:	
			pygame.display.flip()
		
		if test[1] == '~*~':
			return True
		else:
			return False
	
	def render_load(self,num,progress=None):
		
		s = pygame.Surface((640,360))
		
		s.fill((48,48,48)) #paint it grey(to clear the screen)
		
		if num == 0:
			string = 'Looking for saved data... '
		elif num == 1:
			string = 'Loading world data...'
		elif num == 2:
			string = 'Nothing found...'
		elif num == 3:
			string = 'Generate overworld...'
		elif num == 4:
			string = 'Generate caves...'
		elif num == 5:
			string = 'Saving...'
		elif num == 6:
			string = 'Loading time data...'
		elif num == 7:
			string = 'Loading player data...'
		elif num == 8:
			string = 'Set time...'
		elif num == 9:
			string = 'Generate player...'
		elif num == 10:
			string = 'Making time related changes...'
		elif num == 11:
			string = 'Something has gone wrong...'	
		elif num == 12:
			string = 'Zzzzzzzzzz'
		elif num == 13:
			string = 'Generate deus ex machina...'
		elif num == 14:
			string = 'Loading deus ex machina...'
		elif num == 15:
			string = 'Generate grot...'
		elif num == 16:
			string = 'Generate elfish fortress...'
		elif num == 17:
			string = 'Generate orcish mines...'
		elif num == 18:
			string = 'Generate desert...'
		elif num == 19:
			string = 'Initialize level...'
		
		######add more here
		
		if low_res == False:
			posx = 150
			posy = 200
		else:
			posx=50
			posy= 100
		
		image = self.font.render(string,1,(255,255,255))
		s.blit(image,(posx,posy))
		
		if progress != None:
			s.blit(gra_files.gdic['display'][20],(posx-50,posy+20))
		
			help_sur = pygame.Surface((((progress*320)/100),12))
			help_sur.fill((255,0,255))
			help_sur.blit(gra_files.gdic['display'][21],(0,0))
			help_sur.set_colorkey((255,0,255),pygame.RLEACCEL)	
			help_sur = help_sur.convert_alpha()
		
			s.blit(help_sur,(posx-50,posy+20))
		
		if low_res == False:
			s = pygame.transform.scale(s,(self.displayx,self.displayy))
		
		self.screen.blit(s,(0,0))
			
		pygame.display.flip()
			
	def render_built(self,xmin,xmax,ymin,ymax,style):
		
		if low_res == False:
			start_pos_x = 240 #the center of the main map view
			start_pos_y = 180
		else:
			start_pos_x = 152 #the center of the main map view
			start_pos_y = 122
		
		price = 0
		
		self.render(0, False)
		
		s = pygame.Surface((640,360))
		s.fill((255,0,255))
		
		if style == 'wall':
			
			for y in range (-ymin,ymax+1):
				for x in range (-xmin,xmax+1):
				
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] == 0:
						built_here = 1
						price += 2
					elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
						built_here = 2
						price += 1
					else: 
						built_here = 0
						
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
						if built_here == 1:
							price -= 2 
						elif built_here == 2:
							price -= 1
						built_here = 0
							
					if built_here != 0:
					
						if x == xmax or x == -xmin or y == ymax or y == -ymin:
							if x == xmax or x == -xmin:
								if built_here == 1:
									s.blit(gra_files.gdic['built'][1],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_true here
								elif built_here == 2:
									s.blit(gra_files.gdic['built'][6],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_over here
							if y == ymax or y == -ymin:
								if built_here == 1:
									s.blit(gra_files.gdic['built'][1],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_true here
								elif built_here == 2:
									s.blit(gra_files.gdic['built'][6],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_over here
						else:
							
							None
									
					else:
					
						if x == xmax or x == -xmin or y == ymax or y == -ymin:
							if x == xmax or x == -xmin:
								s.blit(gra_files.gdic['built'][0],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_false here
					
							if y == ymax or y == -ymin:
								s.blit(gra_files.gdic['built'][0],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_false here
						else:
								None
		
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Build Walls~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
		
			# render wood needed
		
			wood_need = int(price/3) 
			if wood_need == 0:
				wood_need = 1
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' 
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
		
			stone_need = int(price/2)
			if stone_need == 0:
				stone_need = 1
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' 
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']ch. Size ['+key_name['b']+']ch. Mode' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!' 
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
		elif style == 'floor':
			
			for y in range (-ymin,ymax+1):
				for x in range (-xmin,xmax+1):
				
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] == 0:
						built_here = 1
						price += 2
					elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
						built_here = 2
						price += 1
					else: 
						built_here = 0
						
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
						if built_here == 1:
							price -= 2 
						elif built_here == 2:
							price -= 1
						built_here = 0
							
					if built_here != 0:
					
						
						if built_here == 1:
							s.blit(gra_files.gdic['built'][5],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_true here
						elif built_here == 2:
							s.blit(gra_files.gdic['built'][7],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_over
									
					else:
					
						s.blit(gra_files.gdic['built'][4],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_false here
		
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
			
			# render mode name
			
			name = '~Build Floor~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render wood needed
		
			wood_need = int(price/2) 
			if wood_need == 0:
				wood_need = 1
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' 
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
		
			stone_need = int(price/3)
			if stone_need == 0:
				stone_need = 1
		
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' 
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']ch. Size ['+key_name['b']+']ch. Mode' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
		
		elif style == 'Door':
			
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].civilisation == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] == 0:
				built_here = 1
				price += 2
			elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].civilisation == True:
				built_here = 2
				price += 1
			else: 
				built_here = 0
						
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == False:
				if built_here == 1:
					price -= 2 
				elif built_here == 2:
					price -= 1
				built_here = 0
			
			if built_here != 0:
				if built_here == 1:
					s.blit(gra_files.gdic['built'][3],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #door_true here
				elif built_here == 2:
					s.blit(gra_files.gdic['built'][8],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #door_over
				
			else:
				s.blit(gra_files.gdic['built'][2],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #door_false here		
		
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Built Door~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render wood needed
				
			wood_need = price
		
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' 
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
		
			stone_need = 0
		
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' 
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']ch. Pos. ['+key_name['b']+']ch. Mode' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			pygame.display.flip()
		
		elif style == 'Stair up':

			if player.pos[2] > 0:
					
				if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].replace == None and world.maplist[player.pos[2]-1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False:
					build_here = 0
				else: 
					build_here = 1
							
				if build_here == 0:
					s.blit(gra_files.gdic['built'][10],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up true icon here
				else:
					s.blit(gra_files.gdic['built'][11],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up false icon here
			else:
				s.blit(gra_files.gdic['built'][11],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up false icon here
			
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Built stair up~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render wood needed
				
			wood_need = 10 
		
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' 
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
		
			stone_need = 40
		
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' 
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']ch. Pos. ['+key_name['b']+']ch. Mode' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			pygame.display.flip()
			
		elif style == 'Stair down':
			
			if player.pos[2] < 15:
				
				if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].replace == None and world.maplist[player.pos[2]+1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False:
					build_here = 0
				else: 
					build_here = 1
							
				if build_here == 0:
					s.blit(gra_files.gdic['built'][12],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up true icon here
				else:
					s.blit(gra_files.gdic['built'][13],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up false icon here
			else:
				s.blit(gra_files.gdic['built'][12],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up false icon here
			
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Built stair down~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render wood needed
				
			wood_need = 10 
		
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' 
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
			if player.pos[2] > 0:
				stone_need = 40
			else:
				stone_need = 15
		
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' 
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']ch. Pos. ['+key_name['b']+']ch. Mode' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			pygame.display.flip()
		
		elif style == 'Agriculture':
			
			for y in range (-ymin,ymax+1):
				for x in range (-xmin,xmax+1):
				
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] == 0:
						built_here = 1
						price += 1
					elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
						built_here = 2
						price += 1
					else: 
						built_here = 0
						
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
						if built_here == 1:
							price -= 2 
						elif built_here == 2:
							price -= 1
						built_here = 0
							
					if built_here != 0:
					
						
						if built_here == 1:
							s.blit(gra_files.gdic['built'][15],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_true here
						elif built_here == 2:
							s.blit(gra_files.gdic['built'][16],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_over
									
					else:
					
						s.blit(gra_files.gdic['built'][14],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_false here
		
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
			
			# render mode name
			
			name = '~Build Agriculture~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render seeds needed
		
			seed_need = price 
			if seed_need == 0:
				seed_need = 1
			wood_need = seed_need
			stone_need = 0
			wood_string = 'Seeds: ' + str(seed_need) + '(' + str(player.inventory.materials.seeds) + ')' 
		
			posx = 120
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']ch. Size ['+key_name['b']+']ch. Mode' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
					
		elif style == 'remove':
			
			for y in range (-ymin,ymax+1):
				for x in range (-xmin,xmax+1):
				
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == True:
						remove_here = 0
					else: 
						remove_here = 1
							
					if remove_here == 0:
						s.blit(gra_files.gdic['built'][9],(start_pos_x+(x*32),start_pos_y+(y*32))) #remove icon here
					else:
						None
			
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Remove~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render ---
				
			wood_string = '---' 
		
			posx = 120
			posy = 15
		
			wood_image = self.font.render(wood_string,1,(255,255,255))
			
			s.blit(wood_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']ch. Size ['+key_name['b']+']ch. Mode' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']REMOVE!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			wood_need = 0
			stone_need = 0
		
		if game_options.mousepad == 0 and low_res == False:
			s_help = pygame.Surface((640,360))
			s_help.fill((255,0,255))
			s_help.blit(s,(80,0))
			s = s_help
			
		s.set_colorkey((255,0,255),pygame.RLEACCEL)	
		s = s.convert_alpha()
		if low_res == False:
			s = pygame.transform.scale(s,(self.displayx,self.displayy))
		
		self.screen.blit(s,(0,0))
		
		pygame.display.flip()
		
		return (wood_need,stone_need)
		
	def render_request(self,line1,line2,line3):
		#this function just renders 3 lines of text in the textbox
		
		self.render(0, True)
		
		if low_res == False:
			s = pygame.Surface((640,360))
		else:
			s = pygame.Surface((320,240))
		
		s.fill((255,0,255))
		
		s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
		# render lines
			
		line1_image = self.font.render(line1,1,(255,255,255))
			
		posx = 0
		posy = 0
			
		s.blit(line1_image,(posx,posy))
			
		line2_image = self.font.render(line2,1,(255,255,255))
		
		posx = 0
		posy = 20
		
		s.blit(line2_image,(posx,posy))
			
			
		line3_image = self.font.render(line3,1,(255,255,255)) 
		
		posx = 0
		posy = 40
		
		s.blit(line3_image,(posx,posy))
		
		if game_options.mousepad == 0 and low_res == False:
			s_help = pygame.Surface((640,360))
			s_help.fill((255,0,255))
			s_help.blit(s,(80,0))
			s = s_help
		
		s.set_colorkey((255,0,255),pygame.RLEACCEL)	
		s = s.convert_alpha()
		s = pygame.transform.scale(s,(self.displayx,self.displayy))
		self.screen.blit(s,(0,0))
			
		pygame.display.flip()

	def render_map(self,level=0):
		
		run = True
		
		while run:
			
			m = pygame.Surface((max_map_size,max_map_size))
		
			for y in range(0,max_map_size):
				for x in range(0,max_map_size):
					try:
						t_col = world.maplist[level][player.on_map].tilemap[y][x].tile_color
					except:
						level = 0
						t_col = world.maplist[level][player.on_map].tilemap[y][x].tile_color
					
					if x > player.pos[0]-2 and x < player.pos[0]+2 and y > player.pos[1]-2 and y < player.pos[1]+2 and level == player.pos[2]: #mark players pos
						m.blit(gra_files.gdic['tile1']['white'],(x,y))
					else:
						if world.maplist[level][player.on_map].known[y][x] == 1:
							m.blit(gra_files.gdic['tile1'][t_col],(x,y))
						elif world.maplist[level][player.on_map].known[y][x] == 0:
							m.blit(gra_files.gdic['tile1']['black'],(x,y))
						else:
							m.blit(gra_files.gdic['tile1']['black'],(x,y))
			if low_res == False:			
				m = pygame.transform.scale(m,(270,270))
			else:
				m = pygame.transform.scale(m,(150,150))
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))

			s.blit(bg,(0,0))
			
			if game_options.mousepad == 1 and low_res == False:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			text = '~Map~ [Press['+key_name['x']+'] to leave'
			text_image = screen.font.render(text,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			lvl_string = 'Level ' + str(level)
			text_image = screen.font.render(lvl_string,1,(0,0,0))
			
			if low_res == False:
				s.blit(text_image,(300,70))
			else:
				s.blit(text_image,(190,50))
			
			text = '['+key_name['ws']+'] - lvl up/down'
			text_image = screen.font.render(text,1,(255,255,255))
			if low_res == True:
				s.blit(text_image,(2,225))
			else:
				s.blit(text_image,(5,335))
			
			if low_res == False:
				s.blit(m,(25,55))
			else:
				s.blit(m,(10,45))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)	
			
			if ui == 'exit':
				global master_loop
				global playing
				global exitgame
				exitgame = True
				screen.render_load(5)
				save(world,player,time,gods,save_path,os.sep)
				screen.save_tmp_png()
				master_loop = False
				playing = False
				run = False
				return('exit')
			
			if ui == 's':
				if level < len(world.maplist)-1:
					level += 1
			elif ui == 'w':
				if level > 0:
					level -=1		
			elif ui == 'x':
				run = False
	
	def render_credits(self):
		
		global master_loop
		
		run = True
		
		while run:
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))

			s.blit(bg,(0,0))
			
			if game_options.mousepad == 1 and low_res == False:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			text = '~Credits~ [Press ['+key_name['x']+'] to leave]'
			text_image = screen.font.render(text,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			if low_res == False:
				credit_items = ('Code & Art: Marian Luck aka Nothing', 'BGM: Inigo del Valle' , 'SFX: Various Artists [mostly CC0]', 'Font: Cody Boisclair', 'Testing: eugeneloza', ' ', 'Special Thanks: taknamay & !freegaming@quitter.se')
			else:
				credit_items = ('Code & Art: Marian Luck aka Nothing', 'BGM: Inigo del Valle' , 'SFX: Various Artists [mostly CC0]', 'Font: Cody Boisclair', 'Testing: eugeneloza', 'Special Thanks: taknamay', '                freegaming@quitter.se')
				
			for i in range (0,len(credit_items)):
			
				text_image = screen.font.render(credit_items[i],1,(0,0,0))
				if low_res == False:
					s.blit(text_image,(21,120+i*25))#blit credit_items
				else:
					s.blit(text_image,(21,46+i*25))#blit credit_items
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
				master_loop = False
				run = False
				return('exit')
			
			if ui == 'x':
				run = False

	def render_text(self,text,replace_keys=True):
 		
		run = True
 		
		while run:
 			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))

			s.blit(bg,(0,0))
			
			if game_options.mousepad == 1 and low_res == False:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			top_text = '[Press ['+key_name['x']+'] to leave]'
			text_image = screen.font.render(top_text,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
							
			for i in range (0,len(text)):
			
				text_image = screen.font.render(text[i],1,(0,0,0))
				if low_res == False:
					s.blit(text_image,(60,80+i*25))#blit credit_items
				else:
					s.blit(text_image,(21,36+i*20))#blit credit_items
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					try:
						screen.render_load(5)
						save(world,player,time,gods,save_path,os.sep)
						screen.save_tmp_png()
						del player
					except:
						None
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'x':
				run = False
							  
	def render_options(self):
		
		run = True
		num = 0
		options_path = save_path
		for c in range(0,5):
			options_path = options_path.replace(os.sep + 'World' + str(c),'')
		
		while run:
			
			if low_res == False:
				if game_options.screenmode == 2:
					winm = 'Screenmode: Fullscreen'
				elif game_options.screenmode == 1:
					winm = 'Screenmode: Windowed(1280X720)'
				else:
					winm = 'Screenmode: Windowed(640X360)'
			else:
				winm = '----------'
				
			
			if game_options.bgmmode == 1:
				audiom = 'BGM: ON'
			else:
				audiom = 'BGM: OFF'
				
			if game_options.sfxmode == 1:
				sfxm = 'SFX: ON'
			else:
				sfxm = 'SFX: OFF'
			
			if game_options.turnmode == 1:
				turnm = 'Gamemode: Semi-Realtime'
			else:
				turnm = 'Gamemode: Turnbased'
			
			if low_res == False:	
				if game_options.mousepad == 1:
					mousem = 'Use Mouse: yes'
				else:
					mousem = 'Use Mouse: no'
			else:
				mousem = '----------'
				
			if game_options.check_version == 1:
				versm = 'Check Version: yes'
			else:
				versm = 'Check Version: no'
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))

			s.blit(bg,(0,0))
			
			text = '~Options~ [Press ['+key_name['e']+'] to choose]'
			text_image = screen.font.render(text,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
		
			menu_items = (winm,audiom,sfxm,turnm,mousem,versm,'Done')
		
			for i in range (0,len(menu_items)):
			
				text_image = screen.font.render(menu_items[i],1,(0,0,0))
				if low_res == False:
					s.blit(text_image,(21,120+i*25))#blit menu_items
				else:
					s.blit(text_image,(21,46+i*25))#blit menu_items
			
			if low_res == False:
				s.blit(gra_files.gdic['display'][4],(0,112+num*25))#blit marker
			else:
				s.blit(gra_files.gdic['display'][4],(0,38+num*25))#blit marker
		
			if game_options.mousepad == 1 and low_res != True:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
				global master_loop
				global playing
				global exitgame
				global player
				exitgame = True
				try:
					save_options(game_options,options_path,os.sep)
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					del player
				except:
					None
				master_loop = False
				playing = False
				run = False
				return('exit')
			
			if ui == 'w':
				num -= 1
				if num < 0:
					num = len(menu_items)-1
				
			if ui == 's':
				num += 1
				if num >= len(menu_items):
					num = 0
			
			if ui == 'x':
				run = False
			
			if ui == 'e':
				
				if num == 0 and low_res == False:
					screen.re_init()
					pygame.display.flip()
					save_options(game_options,options_path,os.sep)
					
				if num == 1:
					if game_options.bgmmode == 1:
						game_options.bgmmode = 0
						pygame.mixer.music.pause()
					else:
						game_options.bgmmode = 1
						pygame.mixer.music.unpause()
						bgm.check_for_song(force_play=True)
						
					save_options(game_options,options_path,os.sep)
						
				if num == 2:
					if game_options.sfxmode == 1:
						game_options.sfxmode = 0
					else:
						game_options.sfxmode = 1
						
					save_options(game_options,options_path,os.sep)
				
				if num == 3:
					if game_options.turnmode == 1:
						game_options.turnmode = 0
					else:
						game_options.turnmode = 1
						
					save_options(game_options,options_path,os.sep)
				
				if num == 4 and low_res == False:
					if game_options.mousepad == 1:
						game_options.mousepad = 0
					else:
						game_options.mousepad = 1
						
					pygame.mouse.set_visible(game_options.mousepad)
						
					save_options(game_options,options_path,os.sep)
				
				if num == 5:
					if game_options.check_version == 1:
						game_options.check_version = 0
					else:
						game_options.check_version = 1
					
					save_options(game_options,options_path,os.sep)
					
				if num == 6:
					save_options(game_options,options_path,os.sep)
					run = False
					
			
	def render_brake(self):
		
		run = True
		num = 0
		global exitgame
		global playing
		global player
		
		while run:
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))

			s.blit(bg,(0,0))

			text = '~Game Paused~ [Press ['+key_name['e']+'] to choose]'
			text_image = screen.font.render(text,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			if player.on_map == 'dungeon_0_0':
				map_name = 'Map (Disabled)'
			else:
				map_name = 'Map'
			
			menu_items = ('Resume',map_name,'Message History','Save and Exit', 'Options',)
		
			for i in range (0,len(menu_items)):
			
				text_image = screen.font.render(menu_items[i],1,(0,0,0))
				if low_res == False:
					s.blit(text_image,(21,120+i*25))#blit menu_items
				else:
					s.blit(text_image,(21,46+i*25))#blit menu_items
			
			if low_res == False:
				s.blit(gra_files.gdic['display'][4],(0,112+num*25))#blit marker
			else:
				s.blit(gra_files.gdic['display'][4],(0,38+num*25))#blit marker
			
			if game_options.mousepad == 1 and low_res != True:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
				
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			if low_res == False:
				s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
		
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'w':
				num -= 1
				if num < 0:
					num = len(menu_items)-1
				
			if ui == 's':
				num += 1
				if num >= len(menu_items):
					num = 0
			
			if ui == 'x':
				run = False
			
			if ui == 'e':
				
				if num == 0:
					run = False
					
				if num == 1:
					if player.on_map != 'dungeon_0_0':
						do = screen.render_map(player.pos[2])
						if do == 'exit':
							run = False 
					
				if num == 2:
					do = message.render_history()
					if do == 'exit':
						run = False
					
				if num == 3:
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					del player
					playing = False
					run = False
					
				if num == 4:
					do = screen.render_options()
					if do == 'exit':
						run = False
											
		return exitgame
	
	def get_choice(self,headline,choices,allow_chancel,style='Default'): 
		
		#this function allows the player to make a coice. The choices-variable is a tulpel with strings. The function returns the number of the chosen string inside the tulpel
		
		run = True
		num = 0
		
		while run:
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			
			if style == 'Default':
				bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			elif style == 'Warning':
				bg.blit(gra_files.gdic['display'][17],(0,0))
				
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))
			
			s.blit(bg,(0,0))
		
			text_image = screen.font.render(headline,1,(255,255,255))
			if low_res == False:
				s.blit(text_image,(5,2))#menue title
			else:
				s.blit(text_image,(0,2))#menue title
		
			menu_items = choices
		
			for i in range (0,len(menu_items)):
			
				text_image = screen.font.render(menu_items[i],1,(0,0,0))
				if low_res == False:
					s.blit(text_image,(21,120+i*25))#blit menu_items
				else:
					s.blit(text_image,(21,46+i*25))#blit menu_items
			
			if allow_chancel == True:
				string = '['+key_name['e']+'] - choose ['+key_name['x']+'] - leave'
				text_image = screen.font.render(string,1,(255,255,255))
				if low_res == True:
					s.blit(text_image,(0,225))
				else:
					s.blit(text_image,(5,335))
				
			else:
				string = '['+key_name['e']+'] - choose'
				text_image = screen.font.render(string,1,(255,255,255))
				if low_res == True:
					s.blit(text_image,(0,225))
				else:
					s.blit(text_image,(5,335))
			
			if style == 'Default':
				if low_res == False:
					s.blit(gra_files.gdic['display'][4],(0,112+num*25))#blit marker
				else:
					s.blit(gra_files.gdic['display'][4],(0,38+num*25))#blit marker
					
			elif style == 'Warning':
				if low_res == False:
					s.blit(gra_files.gdic['display'][18],(0,112+num*25))#blit marker
				else:
					s.blit(gra_files.gdic['display'][18],(0,38+num*25))#blit marker
			
			if game_options.mousepad == 1 and low_res == True:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			else:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			
			if low_res == False:
				s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			screen.screen.blit(s,(0,0))
			
			pygame.display.flip()
		
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					global player
					exitgame = True
					try:
						screen.render_load(5)
						save(world,player,time,gods,save_path,os.sep)
						screen.save_tmp_png()
					except:
						None
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'w':
				num -= 1
				if num < 0:
					num = len(menu_items)-1
				
			if ui == 's':
				num += 1
				if num >= len(menu_items):
					num = 0
				
			if ui == 'e':
				run = False
				return num
				
			if ui == 'x' and allow_chancel == True:
				run = False
				return 'Break' 
		
	def string_input(self, input_message, length):			
			
		run = True
		string = ''
		pos = 0
		x = 0
		y = 0
		
		char_field = (('A','B','C','D','E','F','G','H','a','b','c','d','e','f','g','h'),('I','J','K','L','M','N','O','P','i','j','k','l','m','n','o','p'),('Q','R','S','T','U','V','W','X','q','r','s','t','u','v','w','x'),('Y','Z','y','z','0','1','2','3','4','5','6','7','8','9', '.',','),('(','[','<','{',')',']','>','}','#','+','-','_','*','/','&','%'))
		
		while run:
			
			s = pygame.Surface((640,360))
			
			s.blit(gra_files.gdic['display'][1],(0,0)) #render background
	
			text_image = screen.font.render(input_message,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			num_stars = length - len(string)
			
			star_string = ''
			
			if num_stars > 0:
				
				for i in range (0,num_stars):
					star_string += '*'
			
			shown_string = string + '_' + star_string 
			
			string_image = screen.font.render(shown_string,1,(255,255,255))
			s.blit(string_image,(5,35))#string so far
				
			for i in range (0,5):#blit chars
				for j in range (0,len(char_field[1])):
						
					if i == y and j == x: 
						char_image = screen.font.render(char_field[i][j],1,(255,255,255))
					else:
						char_image = screen.font.render(char_field[i][j],1,(0,0,0))
						
					if low_res == False:		
						s.blit(char_image,(55+(j*20),150+(i*20)))
					else:
						s.blit(char_image,(5+(j*20),90+(i*20)))
			
			if game_options.mousepad == 1 and low_res == False:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			text = '['+key_name['e']+'] - Add Char ['+key_name['x']+'] - Del Char ['+key_name['b']+'] - Done'
			text_image = screen.font.render(text,1,(255,255,255))
			
			if low_res == False:
				s.blit(text_image,(5,335))
			else:
				help_sur = pygame.Surface((320,16))
				help_sur.fill((48,48,48))
				help_sur.blit(text_image,(5,5))
				s.blit(help_sur,(0,224))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			
			screen.screen.blit(s,(0,0))
				
			pygame.display.flip()
						
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
		
			if ui == 'w':
				y -= 1
				if y < 0:
					y = 4
				
			if ui == 's':
				y += 1
				if y > 4:
					y = 0
				
			if ui == 'a':
				x -= 1
				if x < 0:
					x = len(char_field[1])-1
				
			if ui == 'd':
				x += 1
				if x > len(char_field[1])-1:
					x = 0
				
			if ui == 'e':
					
				if pos <= length:
					string += char_field[y][x]
					pos += 1
						
			if ui == 'b':
				run = False
				
			if ui == 'x':
				if pos > 0:
					pos -= 1
					string = string[:pos]
					
		return string
		
	def render_dead(self):
		
		global exitgame
		
		self.reset_hit_matrix()
		
		run = True
		
		while run:
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
			
			s.fill((48,48,48)) #paint it grey(to clear the screen)
		
			text_image = screen.font.render('YOU ARE DEAD!',1,(255,255,255))
			
			if low_res == False:
				s.blit(text_image,(175,60))
			else:
				s.blit(text_image,(75,60))
		
			if player.difficulty == 3: #you play on roguelike mode
				choose_string = '------------- ['+key_name['x']+'] - END GAME'
			else:#you play on a other mode
				choose_string = '['+key_name['e']+'] - RESPAWN ['+key_name['x']+'] - END GAME'  
		
			choose_image = screen.font.render(choose_string,1,(255,255,255))
			
			if low_res == False:
				s.blit(choose_image,(125,200))
			else:
				s.blit(choose_image,(25,200))
			
			if game_options.mousepad == 1 and low_res == False:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			else:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			
			if low_res == False:
				s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			
			screen.screen.blit(s,(0,0))
			
			pygame.display.flip()
		
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					if player.difficulty !=3:
						screen.render_load(5)
						save(world,player,time,gods,save_path,os.sep)
						screen.save_tmp_png()
					else:
						files_to_remove = ('gods.data','player.data','world.data','time.data')
						for i in files_to_remove:
							del_file = save_path + os.sep + i
						try:
							os.remove(del_file)
						except:
							None
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'e' and player.difficulty != 3:
				player.respawn()
				save(world,player,time,gods,save_path,os.sep)
				run = False
			elif ui == 'x':
				player.respawn()
				if player.difficulty != 3:
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
				else:
					files_to_remove = ('gods.data','player.data','world.data','time.data')
					for i in files_to_remove:
						del_file = save_path + os.sep + i
						try:
							os.remove(del_file)
						except:
							None
				run = False
				exitgame = True
					
class maP():
	
	def __init__(self, name, tilemap, visit=False, map_type='overworld',monster_num=1):
		
		self.name = name
		self.known = []
		self.containers = []
		self.tilemap = tilemap
		self.visit = visit
		self.last_visit = 0 #-------test only
		self.map_type = map_type
		self.monster_num = monster_num
		self.build_type = 'Full' #Full: build everything you want, Part: no stairs, None: Buildmode is not callable
		self.thirst_multi_day = 1
		self.thirst_multi_night = 1
		self.no_monster_respawn = False
		self.countdowns = []
		self.npcs = []
		self.monster_plus = 0
		self.monster_count = 0
		
		for y in range (0,max_map_size):
			self.known.append([])
			for x in range (0,max_map_size):
				self.known[y].append(0) 
				
		for y in range (0,max_map_size):
			self.containers.append([])
			for x in range (0,max_map_size):
				self.containers[y].append(0)
				
		for y in range (0,max_map_size):
			self.npcs.append([])
			for x in range (0,max_map_size):
				self.npcs[y].append(0) 
	
	def fill(self, tile):
		for y in range (0,max_map_size):
			for x in range(0,max_map_size):
				self.tilemap[y][x] = deepcopy(tile)
	
	def set_round_frame(self,tile,radius):
		center = int(max_map_size/2)
		for y in range(0,max_map_size):
			for x in range(0,max_map_size):
				range_x = x-center
				range_y = y-center
				if ((range_x**2+range_y**2)**0.5) > radius:
					self.tilemap[y][x] = tile
	
	def drunken_walker(self,startx,starty,tile_replace,num_replace):
		
		num = 1
		x = startx
		y = starty
		
		self.tilemap[y][x] = tile_replace
		
		while num < num_replace:
			#step 0: get possible directions
			dir_list = []
			for n in range(-1,2):
				if x+n < max_map_size-2 and x+n > 2:
					if x+n < max_map_size-7 and x+n > 7:
						count = 5
					else:
						count = min((max_map_size-2)-(x+n),(x+n),3)
						
					count = max(count,1)#only to be sure count < 1	
						
					for c in range(0,count):
						dir_list.append([x+n,y])
				if y+n < max_map_size-2 and y+n > 2:
					if y+n < max_map_size-7 and y+n > 7:
						count = 5
					else:
						count = min((max_map_size-2)-(y+n),(y+n),3)
					
					count = max(count,1)#only to be sure count < 1	
						
					for c in range(0,count):
						dir_list.append([x,y+n])
					
			#step 1: set tile new tile
			ran = random.randint(0,len(dir_list)-1)
			x = dir_list[ran][0]
			y = dir_list[ran][1]
			if self.tilemap[y][x].techID != tile_replace.techID:
				self.tilemap[y][x] = tile_replace
				num += 1
				
	def floating(self,startx,starty,tile_fill,tile_border):
		#its important to use a tile_fill that isn't on the map and a tile_border that is on the map 
		
		run = True
		
		self.tilemap[starty][startx] = deepcopy(tile_fill)
		
		while run:
			
			count = 0
			
			for y in range(0,max_map_size):
				for x in range(0,max_map_size):
					
					if self.tilemap[y][x].techID == tile_fill.techID:
						
						for yy in range(y-1,y+2):
							for xx in range(x-1,x+2):
								
								try:
									if self.tilemap[yy][xx].techID != tile_border.techID and self.tilemap[yy][xx].techID != tile_fill.techID:
										self.tilemap[yy][xx] = deepcopy(tile_fill)
										count += 1
								except:
									None
									
			if count == 0:
				run = False
	
	def get_quarter_size(self,startx,starty):
		
		#this funktion gives back a tulpel with the width and height of a quarter made out of the same tile like the start position
		
		techID = self.tilemap[starty][startx].techID
		
		q_width = 0
		q_height = 0
		
		run_w = True
		run_h = True
		
		while run_w:
			
			if self.tilemap[starty][startx+q_width].techID == techID:
				q_width += 1
			else:
				run_w = False
				
		while run_h:
			
			if self.tilemap[starty+q_height][startx].techID == techID:
				q_height += 1
			else:
				run_h = False
				
		return (q_width,q_height)
			
	def set_frame(self,tile):
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				if x == 0 or x == max_map_size-1 or y == 0 or y == max_map_size-1:
					self.tilemap[y][x] = tile

			
	def cut(self, minx, maxx, miny, maxy, replace):
		#everything that is not between min and mx is replaced abainst a tile
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				if x < minx or x > maxx or y < miny or y > maxy:
					self.tilemap[y][x] = replace 
		
	def imp(self, start_x, start_y, replace_inner, replace_outer, step_min, step_max, circles, replace_except=None): #dig random caves
		
		#was made to generate random caves but dosn't pleased me. maybe this can be used for mazes.(unused atm)
		
		x = start_x
		y = start_y
		
		for l in range (0,circles):
			
			run = True
			
			while run:
				
				direction = random.randint(0,3)
				
				move_x = 0
				move_y = 0
				
				if direction == 0:
					move_y = -1
				elif direction == 1:
					move_x = 1 
				elif direction == 2:
					move_y = 1
				else:
					move_x= -1
					
				length = random.randint(step_min, step_max)
				
				for m in range (0,length):
					
					x = x + move_x
					y = y + move_y
					
					if x <= 1 or x >= 78 or y <= 1 or y >= 78:
						break
						run = False
					
					self.tilemap[y][x] = replace_inner
					
					for b in range (-1,2):
						for a in range (-1,2):
					
							if self.tilemap[y+a][x+b] != replace_outer and self.tilemap[y+a][x+b] != replace_inner and self.tilemap[y+a][x+b] != replace_except:
								self.tilemap[y+a][x+b] = replace_outer
					
				run = False

	def imp_connect(self,xpos,ypos,replace_inner,replace_except=None,except_replacer=None,style='straight'): #conects two or more points
						
		for a in range (0,len(ypos)-1):
			for b in range(0,len(xpos)-1):
				
				y = ypos[a]
				x = xpos[b]
				
				go = True
				direction = 0 #needed for natural ways. jumps between 0 and 1
				
				while go:
					
					try:
						y_goal = ypos[a+1]
						x_goal = xpos[b+1]
				  
					except:
						y_goal = ypos[0]
						x_goal = xpos[0]
						
					if x == x_goal and y == y_goal:
						go = False
						
					if x_goal - x < 0: #find out if you need to go right or left
						x_direction = -1
					else:
						x_direction = 1
						
					if y_goal - y < 0: #find out if you need to go up or down
						y_direction = -1
					else:
						y_direction = 1
					
					if style == 'straight':	
						if x != x_goal:
						
							x = x + x_direction
					
							if self.tilemap[y][x] != replace_except:
								self.tilemap[y][x] = replace_inner
							elif self.tilemap[y][x] == replace_except:
								self.tilemap[y][x] = except_replacer
									
						elif y != y_goal:
						
							y = y + y_direction
						
							if self.tilemap[y][x] != replace_except:
								self.tilemap[y][x] = replace_inner
							elif self.tilemap[y][x] == replace_except:
								self.tilemap[y][x] = except_replacer
								
					elif style == 'natural':
						
						if x != x_goal and direction == 0:
						
							x = x + x_direction
					
							if self.tilemap[y][x] != replace_except:
								self.tilemap[y][x] = replace_inner
							elif self.tilemap[y][x] == replace_except:
								self.tilemap[y][x] = except_replacer
									
						elif y != y_goal and direction == 1:
						
							y = y + y_direction
						
							if self.tilemap[y][x] != replace_except:
								self.tilemap[y][x] = replace_inner
							elif self.tilemap[y][x] == replace_except:
								self.tilemap[y][x] = except_replacer
						
						if direction == 0:
							direction = 1
						elif direction == 1:
							direction = 0
	
	def spawn_monsters(self,depth):
		#This function spawns monsters on the map
		
		print('start spawn')
		
		if self.map_type == 'elfish_fortress':
			monster_max = 0
			for y in range(0,max_map_size):
				for x in range(0,max_map_size):
					if self.tilemap[y][x].techID == tl.tlist['functional'][8].techID:#this is a bed
						monster_max += 1
		else:
			monster_max = (max_map_size*max_map_size)/30
		
		monster_max = int(monster_max * self.monster_num)
		
		if self.map_type == 'grot':
			spawnpoints = self.find_all_moveable(False)
		else:
			spawnpoints = self.find_all_moveable()
		
		del_list = []
		monster_count = self.monster_count
		
		for i in range (0,len(spawnpoints)):
			
			if self.npcs[spawnpoints[i][1]][spawnpoints[i][0]] != 0: #there is a monster here
				spawnpoints[i] = 'del'
				#monster_count += 1#count the monsters that are already on the map
			
		newlist = []
		
		for k in spawnpoints:
			if k != 'del':
				newlist.append(k)
				
		spawnpoints = newlist
			
		monster_max -= monster_count
		
		if monster_max > len(spawnpoints):
			monster_max = len(spawnpoints)
		print(monster_max,monster_count)	
		for k in range(0,monster_max):
			
			ran = random.randint(0,len(ml.mlist[self.map_type])-1)
			ran2 = random.randint(0,len(spawnpoints)-1)
			ran3 = random.randint(0,len(ml.mlist['civilian'])-1)
				
			if self.tilemap[spawnpoints[ran2][1]][spawnpoints[ran2][0]].civilisation == False:#spawn a wild monster
				self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]] = deepcopy(ml.mlist[self.map_type][ran])#deepcopy is used that every monster on the map is saved separate
				self.set_monster_strength(spawnpoints[ran2][0],spawnpoints[ran2][1],depth)
				self.monster_count += 1
				if self.no_monster_respawn == False:
					self.countdowns.append(countdown('spawner',spawnpoints[ran2][1],spawnpoints[ran2][0],random.randint(5,60)))
				try:
					if player.difficulty == 4:
						self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]].AI_style = 'ignore'
				except:
					None
						
			else:#spawn a civilian
				self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]] = deepcopy(ml.mlist['civilian'][ran3])
				self.set_monster_strength(spawnpoints[ran2][1],spawnpoints[ran2][1],depth)
			
			#set monsters personal_id
			
			self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]].personal_id = str(self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]].techID)+'_'+str(spawnpoints[ran2][0])+'_'+str(spawnpoints[ran2][1])+'_'+str(random.randint(0,9999))
			
		print('Spawn success')
			
	def set_monster_strength(self,x,y,z,preset_lvl=None ):
		
		if self.npcs[y][x] != 0:
			
			old_lvl = self.npcs[y][x].lvl
			
			ran = random.randint(1,3)
			if Time_ready == True:
				if player.difficulty == 3:
					base_lvl = 25
				elif player.difficulty == 2:
					base_lvl = 20
				elif player.difficulty == 1:
					base_lvl = 15
				elif player.difficulty == 0:
					base_lvl = 10
				else:
					base_lvl = 0

				time_coeff = int(base_lvl*((time.year-1)*28*12 + time.day_total)/150) #base_lvl levels each 150 days of gameplay # 
			else:
				time_coeff = 0
			
			if self.npcs[y][x].techID == ml.mlist['overworld'][0] or self.npcs[y][x].techID == ml.mlist['angry_monster'][2]: #this is a dryade
				try:
					time_coeff = player.lvl
				except:
					None
			
			monster_lvl = z + ran + self.monster_plus + time_coeff
			
			if monster_lvl >= old_lvl and old_lvl > 0:
				try:
					screen.write_hit_matrix(x,y,12) #render monster_lvl_up
				except:
					None
				
			if preset_lvl != None:
				self.npcs[y][x].lvl = preset_lvl
			else:
				self.npcs[y][x].lvl = monster_lvl
			
			attribute_list =[] 
		
			al = ('p_strength','p_defense','m_strength','m_defense','health')
			a_nr = 0
		
			for c in self.npcs[y][x].attribute_prev:
				for h in range(0,c):
					attribute_list.append(al[a_nr])
				a_nr+=1
		
			for i in range(0,monster_lvl):
				choice = al[random.randint(0,len(al)-1)]
				
				if choice == 'p_strength':
					self.npcs[y][x].basic_attribute.p_strength +=3
				elif choice == 'p_defense':
					self.npcs[y][x].basic_attribute.p_defense +=3
				elif choice == 'm_strength':
					self.npcs[y][x].basic_attribute.m_strength +=3
				elif choice == 'm_defense':
					self.npcs[y][x].basic_attribute.m_defense +=3
				elif choice == 'health':
					self.npcs[y][x].basic_attribute.max_lp +=1
					self.npcs[y][x].lp = self.npcs[y][x].basic_attribute.max_lp	
			
			if old_lvl == 0:
				el = [['spear','sword','axe','hammer'],['rune','wand','rune staff','artefact'],['armor','armor'],['necklace','amulet','talisman'],['ring','ring']]
				e_nr = 0
			
				for q in range(0,len(el)-1):
					ran = random.randint(0,len(el[q])-1)
					
					if self.npcs[y][x].worn_equipment[q] == 1:
						help_equipment = item_wear(el[q][ran],random.randint(0,min((z*3),21)),random.randint(-2,2))
					
						self.npcs[y][x].basic_attribute.p_strength += help_equipment.attribute.p_strength
						self.npcs[y][x].basic_attribute.p_defense += help_equipment.attribute.p_defense
						self.npcs[y][x].basic_attribute.m_strength += help_equipment.attribute.m_strength
						self.npcs[y][x].basic_attribute.m_defense += help_equipment.attribute.m_defense
						self.npcs[y][x].basic_attribute.luck += help_equipment.attribute.luck
				
	def AI_move(self):
		#This function moves all monsters that are 7 or less fields away from the player.
		#It dosn't move all monsters to save performance
		
		ymin = player.pos[1]-7
		if ymin < 0:
			ymin = 0
		xmin = player.pos[0]-7
		if xmin < 0:
			xmin = 0
		ymax = player.pos[1]+8
		if ymax > max_map_size:
			ymax = max_map_size
		xmax = player.pos[0]+8
		if xmax > max_map_size:
			xmax = max_map_size
			
		for y in range (ymin,ymax):#reset the move_done switches
			for x in range (xmin,xmax):
				
				if self.npcs[y][x] != 0:
					if self.npcs[y][x].lp > 0:
						self.npcs[y][x].move_done = 0
					else:
						test = False
						while test == False:
							test = self.monster_die(x,y)	
		
		for y in range (ymin,ymax):
			for x in range (xmin,xmax):
				
				
				if self.npcs[y][x] != 0 and self.npcs[y][x].move_done == 0:#if there is a monster at this place
						
						#I. Get possible fields for a move
						
					moves = [(x,y)]
						
					yy = (-1,0,0,1)
					xx = (0,-1,1,0)
						
					for i in range (0,4):
							
						try:
								
							monster_move_groups = self.npcs[y][x].move_groups
							tile_move_group = self.tilemap[y+yy[i]][x+xx[i]].move_group
							
							move_group_check = False
							
							for j in range(0,len(monster_move_groups)):
								if monster_move_groups[j] == tile_move_group:
									move_group_check = True
									
							if self.npcs[y+yy[i]][x+xx[i]] == 0:
								npc = False
							else:
								npc = True
									
							if self.tilemap[y+yy[i]][x+xx[i]].techID == tl.tlist['functional'][1].techID or self.tilemap[y+yy[i]][x+xx[i]].techID == tl.tlist['functional'][2].techID: #this is a stair up/down
								stair = True
							else:
								stair = False
									
							if x + xx[i] == player.pos[0] and y + yy[i] == player.pos[1]:
								playerpos = True
							else:
								playerpos = False
							
							if move_group_check == True and npc == False and stair == False and playerpos == False:
									
								moves.append((x+xx[i],y+yy[i]))
									
									
						except:
							print('Debug:Error')
					
						#II. Find out which possible move leads to which distance between monster and player
					distances = []
					
					for j in range (0,len(moves)):
						
						a = player.pos[0] - moves[j][0]
						b = player.pos[1] - moves[j][1]
						
						c = (a**2 + b**2)**0.5 # this is just the good old pythagoras (c² = a² + b²)
						
						distances.append(c)
						
						#III. Choose the right move (or special action)
					
					do_move = 'foo'
					
					if self.npcs[y][x].AI_style == 'hostile':
						
						if self.npcs[y][x].lp < self.npcs[y][x].basic_attribute.max_lp and player.lp > 2 and self.npcs[y][x].num_special > 0 :#this is a defensive situation for the monster
							
							ran = random.randint(0,99)
							
							if ran < self.npcs[y][x].def_teleport and self.npcs[y][x].move_done != 1:
								moves = self.find_all_moveable(ignore_player_pos = False)
								if moves != False:
									if len(moves) == 1:
										pos_num = 0
									else:
										pos_num = random.randint(0,len(moves)-1)
										
									self.npcs[y][x].move_done = 1
									self.npcs[y][x].num_special -= 1
									tp_string = 'A ' + self.npcs[y][x].name + ' teleports.'
									message.add(tp_string)
									screen.write_hit_matrix(x,y,7)
									self.npcs[moves[pos_num][1]][moves[pos_num][0]] = self.npcs[y][x]
									self.npcs[y][x] = 0
							
							ran = random.randint(0,99)
							if self.npcs[y][x] != 0:		
								if ran < self.npcs[y][x].def_flee and self.npcs[y][x].move_done != 1 and self.npcs[y][x].lp < self.npcs[y][x].basic_attribute.max_lp:
									flee_string = 'A ' + self.npcs[y][x].name + ' turns to flee.'
									message.add(flee_string)
									self.npcs[y][x].AI_style = 'flee'
									self.npcs[y][x].move_done = 1
									self.npcs[y][x].num_special -= 1
							
								ran = random.randint(0,99)
						
								if ran < self.npcs[y][x].def_potion and self.npcs[y][x].move_done != 1:
									if self.npcs[y][x].lp < self.npcs[y][x].basic_attribute.max_lp:
										potion_string = 'A ' + self.npcs[y][x].name + ' quaffes a potion of healing.'
										message.add(potion_string)
										screen.write_hit_matrix(x,y,6)
										lp = min(self.npcs[y][x].basic_attribute.max_lp, self.npcs[y][x].lp+7)
										self.npcs[y][x].lp = lp
										self.npcs[y][x].move_done = 1
										self.npcs[y][x].num_special -= 1
									
						if self.npcs[y][x] != 0:
							if distances[0] > 1 and self.npcs[y][x].move_done != 1: #moves[0] is always the position of the monster right now, so distances 0 is always it's distance towards the player
							
								ran = random.randint(0,99)
								
								if ran < self.npcs[y][x].spawn_skeleton or ran < self.npcs[y][x].spawn_shadow:
									xlist = []
									ylist = []
									for yy in range(y-1,y+2):
										for xx in range(x-1,x+2):
											if self.tilemap[yy][xx].move_group == 'soil' and self.npcs[yy][xx] == 0:
												xlist.append(xx)
												ylist.append(yy)
												
									if len(xlist) == len(ylist) and len(xlist) > 0:
										if len(xlist) > 1:
											num = random.randint(0,len(xlist)-1)
										else:
											num = 0
									
										if self.npcs[y][x].spawn_skeleton > 0 and self.npcs[y][x].move_done != 1 and self.npcs[y][x].num_special > 0:
											self.npcs[ylist[num]][xlist[num]] = deepcopy(ml.mlist['special'][7])
											self.npcs[ylist[num]][xlist[num]].personal_id = self.npcs[y][x].personal_id + '_child'
											self.set_monster_strength(x,y,player.pos[2])
											mes = 'A ' + self.npcs[y][x].name + ' summones a skeleton.'
											message.add(mes)
											screen.write_hit_matrix(xlist[num],ylist[num],7)
											self.npcs[y][x].move_done = 1
											self.npcs[y][x].num_special -= 1
									
										if self.npcs[y][x].spawn_shadow > 0 and self.npcs[y][x].move_done != 1 and self.npcs[y][x].num_special > 0:
											self.npcs[ylist[num]][xlist[num]] = deepcopy(ml.mlist['special'][8])
											self.npcs[ylist[num]][xlist[num]].personal_id = self.npcs[y][x].personal_id + '_child'
											self.set_monster_strength(x,y,player.pos[2])
											mes = 'A ' + self.npcs[y][x].name + ' summones a shadow.'
											message.add(mes)
											screen.write_hit_matrix(xlist[num],ylist[num],7)
											self.npcs[y][x].move_done = 1
											self.npcs[y][x].num_special -= 1
									
								if x == player.pos[0] or y == player.pos[1]:
									straight_line = True
								else:
									straight_line = False
							
								if straight_line == True and self.npcs[y][x].range_shoot != 0 and distances[0] < 5:
									#Step 0: Random
									
									if ran < self.npcs[y][x].range_shoot:
										#Step 1: find the right direction
										if y > player.pos[1]:
											y_dir = -1
										elif y < player.pos[1]:
											y_dir = 1
										else:
											y_dir = 0
											
										if x > player.pos[0]:
											x_dir = -1
										elif x < player.pos[0]:
											x_dir = 1
										else:
											x_dir = 0
										
										#Step 2: Check for borders
										
										run = True
										count = 1
										fire_free = True 
										
										while run:
											cx = x + (count*x_dir)
											cy = y + (count*y_dir)
											
											if self.tilemap[cy][cx].transparency == False:
												fire_free = False
												run = False
											
											count +=1
												
											if cx == player.pos[0] and cy == player.pos[1]:
												run = False
											
										#Step 3: Fire!
										if fire_free == True:
											run = True
											count = 1
											sfx.play('fire')
										
											while run:
												xx = x + (count*x_dir)
												yy = y + (count*y_dir)
											
												if xx != player.pos[0] or yy != player.pos[1]:
													screen.write_hit_matrix(xx,yy,2)
													if self.tilemap[yy][xx].transparency == False:
														run = False
												else:
													player.monster_attacks(x,y)
													run = False
											
												count += 1
												self.npcs[y][x].move_done = 1
								
								if self.npcs[y][x].move_done == 0:
								
									if len(moves) > 0:#if no move is possible at least the 'move' of stay still must remain
										good_moves = []
										for k in range (0, len(moves)):
											if distances[k] < distances[0]:#if the possible move makes the distance between player and monster smaller
												good_moves.append(moves[k])
									else:
										good_moves = moves
								
									if len(good_moves) == 0:
										good_moves = moves
								
									if len(good_moves) > 1:
										ran = random.randint(0,len(good_moves)-1)
									else:
										ran = 0
								
									do_move = good_moves[ran]
						
							else:
								if self.npcs[y][x].move_done == 0:
									#the most important thing about stealing monsters is that their default corps_style has to be 'thief' and their corps_lvl has to be 0. Otherwise they would not work proper.
									if player.inventory.materials.gem > 0:
										ran = random.randint(0,99)
										if ran < self.npcs[y][x].close_steal:
											player.inventory.materials.gem -= 1
											self.npcs[y][x].corps_lvl += 1
											screen.write_hit_matrix(player.pos[0],player.pos[1],8)
											screen.write_hit_matrix(x,y,9)
											sfx.play('steal')											
											steal_string = 'A ' + self.npcs[y][x].name + ' steals a gem from you.'
											message.add(steal_string)
											self.npcs[y][x].move_done = 1#set the move_done switch on
									
									if self.npcs[y][x].move_done == 0:
										#casting flames
										ran = random.randint(0,99)
										if ran < self.npcs[y][x].close_flame and self.npcs[y][x].num_special > 0:
											#Step 0: Check if any (other) monsters are near by
											monster_num = 0
											for yy in range(y-1,y+2):
												for xx in range(x-1,x+2):
													if self.npcs[yy][xx] != 0:
														monster_num += 1
													
											if monster_num == 1:#there is no other monster near by
												
												num_flames = 0
												
												for yyy in range(y-1,y+2):
													for xxx in range(x-1,x+2):
														if xxx != x or yyy != y:
															if self.tilemap[yyy][xxx].replace == None and self.tilemap[yyy][xxx].move_group != 'solide' and self.tilemap[yyy][xxx].move_group != 'low_liquid' and self.tilemap[yyy][xxx].move_group != 'swim':
																replace = self.tilemap[yyy][xxx]
																self.tilemap[yyy][xxx] = deepcopy(tl.tlist['effect'][4])
																self.tilemap[yyy][xxx].replace = replace
																self.countdowns.append(countdown('flame',xxx,yyy,2))
																num_flames+=1	
																											
												if num_flames > 0:
													flame_string = 'A '+ self.npcs[y][x].name + ' casts a flame spell!'
													message.add(flame_string)
													self.npcs[y][x].num_special -= 1
													self.npcs[y][x].move_done = 1
											
									if self.npcs[y][x].move_done == 0:		
										player.monster_attacks(x,y)
										self.npcs[y][x].move_done = 1#set the move_done switch on
					
					elif self.npcs[y][x].AI_style == 'flee':
						
						if distances[0] < 2: #moves[0] is always the position of the monster right now, so distances 0 is always it's distance towards the player
								
							if len(moves) > 1:
								ran = random.randint(0,len(moves)-1)
							else:
								ran = 0
								
							do_move = moves[ran]
						
						else:
							
							if len(moves) > 0:#if no move is possible at least the 'move' of stay still must remain
								
								good_moves = []
								
								for k in range (0, len(moves)):
									if distances[k] > distances[0] or distances[k] == distances[0]:#if the possible move makes the distance between player and monster bigger or at least the same
										good_moves.append(moves[k])
							else:
								good_moves = moves
									
							if len(good_moves) == 0:
								good_moves = moves
								
							if len(good_moves) > 1:
								ran = random.randint(0,len(good_moves)-1)
							else:
								ran = 0
								
							do_move = good_moves[ran]
							
					
					elif self.npcs[y][x].AI_style == 'ignore':
						
						if len(moves) > 1:
							ran = random.randint(0,len(moves)-1)
						else:
							ran = 0
								
						do_move = moves[ran]
							
					#IV. Move the monster
					if do_move != 'foo':
						
						border = random.randint(1,9)
						
						if border > self.npcs[y][x].move_border:
							
							self.npcs[y][x].move_done = 1#set the move_done switch on
							helper = self.npcs[y][x]#copy the monster
							self.npcs[y][x] = 0 #del the monster at the old position
							self.npcs[do_move[1]][do_move[0]] = helper# set monster to the new position
	
	def monster_die(self,x,y):
		#this function is called when the player kills a monster. the x and the y variables are to define the location of the monster
		
		die_mess = 'The ' + self.npcs[y][x].name + ' vanishes!'
		
		if self.tilemap[y][x].replace == None and self.tilemap[y][x].drops_here: #only on empty fields corps can be spawned
			
			if self.npcs[y][x].corps_style == 'dryade' and self.tilemap[y][x].techID != tl.tlist['misc'][0].techID and self.tilemap[y][x].can_grown: #dryades can leave behind a seppling when they are killed(corpse_lvl dosn't matter)/low water isn't allowed
				
				coin = random.randint(0,99)
				
				if coin < 50:#there is a chance of 50%
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = tl.tlist['local'][10]#<---sepling
					self.tilemap[y][x].replace = replace
					
					die_mess = 'The ' + self.npcs[y][x].name + ' turns into a new tree!'
					 
			elif self.npcs[y][x].corps_style == 'troll' and self.tilemap[y][x].techID != tl.tlist['misc'][0]: #trolls can leave behind a rock when they are killed(corpse_lvl dosn't matter)/low water isn't allowed
				
				coin = random.randint(0,99)
				
				if coin < 50:#there is a chance of 50%
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['local'][14])#<---rock
					self.tilemap[y][x].replace = replace
					
					die_mess = 'The ' + self.npcs[y][x].name + ' turns to stone!'
					
			elif self.npcs[y][x].corps_style == 'human': #humanoid monsters can leave behind humanoid remains when they die. the corps_lvl says how much items are stored inside them
				
				coin = random.randint(0,99)
				
				if coin < 15:#there is a chance of 15%
					die_mess = 'The ' + self.npcs[y][x].name + ' dies!'
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['functional'][6])#<--humanoid remains
					self.tilemap[y][x].replace = replace
					
					items = []
					
					max_items = max(1,self.npcs[y][x].corps_lvl)
					
					for i in range (0, max_items):
						#possible drops of a humanoid monster are equipment items and food items
						
						coin = random.randint(0,99)
						
						if coin < 65: #there is a chance of 65% that a item becomes a eqipment item
							
							material = random.randint(0,20) #all materials are allowed
							classes = ('spear','sword','axe','hammer','shoes','cuisse','helmet','armor','wand','rune','rune staff','artefact','ring','amulet','necklace','talisman','pickaxe')
							kind = classes[random.randint(0,len(classes)-1)]#all classes of objects are allowed
							plus = random.randint(-2,+2)# a plus between -2 and +2 is possible
							state = random.randint(10,85)#the state of this used objects will always be between 10% and 80%
							curse = random.randint(0,2)#all curse-states are allowed from cursed to blessed
 							
							item = item_wear(kind,material,plus,state,curse)
							
						elif coin < 68: #there is a chance of 3% to drop a simple blueprint
							
							blueprint = random.randint(15,20)
							item = deepcopy(il.ilist['misc'][blueprint])
						
						elif coin < 80: #there is a	chance of 12% to drop a torch:
							
							item = deepcopy(il.ilist['misc'][44])
							
						else:
							
							item = deepcopy(il.ilist['food'][random.randint(0,len(il.ilist['food'])-1)])
							
						items.append(item)
					
					self.containers[y][x] = container(items)
			
			elif self.npcs[y][x].corps_style == 'animal': #humanoid monsters can leave behind humanoid remains when they die. the corps_lvl says how much items are stored inside them
				
				coin = random.randint(0,99)
				
				if coin < 15:#there is a chance of 15%
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['functional'][21])#<--animal remains
					self.tilemap[y][x].replace = replace
					
					items = []
					
					max_items = max(1,self.npcs[y][x].corps_lvl)
					
					for i in range (0, max_items):
						#animals drop flesh. the corpslvl says how much
							
						items.append(deepcopy(il.ilist['food'][9]))#<---raw meat
						
					self.containers[y][x] = container(items)
					
					die_mess = 'The ' + self.npcs[y][x].name + ' dies!'
			
			elif self.npcs[y][x].corps_style == 'scrollkeeper': #scrollkeepers can leave behind humanoid remains with scrolls and spellbooks when they die. the corps_lvl says how much items are stored inside them
				
				coin = random.randint(0,99)
				
				if coin < 10:#there is a chance of 10%
					die_mess = 'The ' + self.npcs[y][x].name + ' dies!'
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['functional'][6])#<--humanoid remains
					self.tilemap[y][x].replace = replace
					
					items = []
					
					max_items = max(1,self.npcs[y][x].corps_lvl)
					
					for i in range (0, max_items):
						#possible drops of a scrollkeeper are scrolls and spellbooks
						
						coin = random.randint(0,99)
						
						if coin < 75: #there is a chance of 75% that a item becomes a scroll
							
							scrolls = (il.ilist['misc'][25],il.ilist['misc'][27],il.ilist['misc'][29],il.ilist['misc'][31],il.ilist['misc'][33],il.ilist['misc'][35],il.ilist['misc'][37],il.ilist['misc'][45])
							
							ran = random.randint(0,len(scrolls)-1)
							
							item = deepcopy(scrolls[ran])
								
						else:
							
							books = (il.ilist['misc'][26],il.ilist['misc'][28],il.ilist['misc'][30],il.ilist['misc'][32],il.ilist['misc'][34],il.ilist['misc'][36],il.ilist['misc'][38],il.ilist['misc'][46])
							
							ran = random.randint(0,len(books)-1)
							
							item = deepcopy(books[ran])
							
						items.append(item)
						
					self.containers[y][x] = container(items)
			
			elif self.npcs[y][x].corps_style == 'miner':
				
				if self.npcs[y][x].techID == ml.mlist['special'][0].techID:#this is a vase
					die_mess = 'The vase shatters.'  
				
				if self.tilemap[y][x].replace == None:
					
					ran = random.randint(0,99)
					
					if ran <= self.npcs[y][x].corps_lvl: #for miners the corps_lvl determinates the chance of getting a gem
						
						replace = self.tilemap[y][x]
						self.tilemap[y][x] = deepcopy(tl.tlist['misc'][9])#set a lost gem
						self.tilemap[y][x].replace = replace
					
					elif ran <= self.npcs[y][x].corps_lvl*4:#for miners the corps_lvl determinates the chance of getting some ore. Its the chance to get a gem * 3 
						
						replace = self.tilemap[y][x]
						self.tilemap[y][x] = deepcopy(tl.tlist['misc'][11])#set a lost ore
						self.tilemap[y][x].replace = replace
			
			elif self.npcs[y][x].corps_style == 'thief':
				
				if self.tilemap[y][x].replace == None and self.npcs[y][x].corps_lvl > 0:

					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['misc'][9])#set a lost gem
					self.tilemap[y][x].replace = replace
					self.tilemap[y][x].conected_resources = ('gem',self.npcs[y][x].corps_lvl)#for thiefs the corps lvl determinates the number of gems they are dropping
			
			elif self.npcs[y][x].corps_style == 'reset_parent':
				
				parent_id = self.npcs[y][x].personal_id.replace('_child','')
				
				for yy in range(0,max_map_size):
					for xx in range(0,max_map_size):
						if self.npcs[yy][xx] != 0:
							if self.npcs[yy][xx].personal_id == parent_id:
								self.npcs[yy][xx].num_special += 1
							
			elif self.npcs[y][x].corps_style == 'kill_childs':
				
				child_id = self.npcs[y][x].personal_id + '_child'
				
				for yy in range(0,max_map_size):
					for xx in range(0,max_map_size):
						if self.npcs[yy][xx] != 0:
							if self.npcs[yy][xx].personal_id == child_id:
								self.npcs[yy][xx] = 0
					
			elif self.npcs[y][x].corps_style == 'vase':
				
				die_mess = 'The vase shatters and monsters jump out.'
				
				for yy in range(y-1,y+2):
					for xx in range(x-1,x+2):
						
						if yy != player.pos[1] or xx!= player.pos[0]:
							if self.npcs[yy][xx] == 0 and self.tilemap[yy][xx].move_group == 'soil' and self.tilemap[yy][xx].damage == 0:
								self.npcs[yy][xx] = deepcopy(ml.mlist['special'][2])#set vase monsters
								self.set_monster_strength(xx,yy,player.pos[2])
								if player.difficulty == 4:
									self.npcs[yy][xx].AI_style = 'ignore'
								
			elif self.npcs[y][x].corps_style == 'mimic':
				
				die_mess = 'The mimic wakes up.'
						
			elif self.npcs[y][x].corps_style == 'vanish':
				
				ran = random.randint(0,99)
					
				if ran <= self.npcs[y][x].corps_lvl: #the corps_lvl determinates the chance of getting a present
					
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['misc'][13])#set a present
					self.tilemap[y][x].replace = replace
						
					item_ran = random.randint(0,99)
						
					if item_ran < 25:
							
						self.containers[y][x] = container([il.ilist['misc'][43]])#set a heavy bag
					
					elif item_ran < 50:
						
						clothe_list = [il.ilist['clothe'][0],il.ilist['clothe'][1],il.ilist['clothe'][2]]
						
						if self.map_type == 'desert':
							clothe_list.append(il.ilist['clothe'][5])#add neko ears
						elif self.map_type == 'orcish_mines':
							clothe_list.append(il.ilist['clothe'][7])#add orćish helmet
						else:
							clothe_list.append(il.ilist['clothe'][6])#add simple hat
						
						choose_ran = random.randint(0,len(clothe_list)-1)	
						self.containers[y][x] = container([clothe_list[choose_ran]])
							
					elif item_ran < 95:
							
						r = random.randint(3,7)
							
						self.containers[y][x] = container([il.ilist['misc'][r]])#set a workbench
							
					else:
							
						self.containers[y][x] = container([il.ilist['misc'][40]])#set a heart-shaped crystal
						
						
				
			############ADD MORE HERE###############
		
		if self.npcs[y][x].corps_style == 'mimic':
			self.npcs[y][x] = deepcopy(ml.mlist['special'][4])#set a mimic
			self.set_monster_strength(x,y,player.pos[2])
			if player.difficulty == 4:
				self.npcs[y][x].AI_style = 'ignore'
		else:
			self.npcs[y][x] = 0 #always del the monster if it is no mimic
		self.make_monsters_angry(x,y,'kill')
		self.monster_count -= 1
		print(die_mess, self.monster_count)
		message.add(die_mess)
		return True
	
	def make_shops(self):
		
		num = int((max_map_size*max_map_size) / (50*50))
		
		for i in range (0,num):
			
			poses = self.find_all_moveable(False,False)
			ran = random.randint(0,len(poses)-1)
			pos = poses[ran]
			
			x = pos[0]
			y = pos[1]
			
			for yy in range(y-2,y+3):
				for xx in range(x-2,x+3):
					
					self.npcs[yy][xx] = 0 #always del the monsters
					
					if xx == x-2 or xx == x+2 or yy == y-2 or yy == y+2:
						self.tilemap[yy][xx] = deepcopy(tl.tlist['shop'][1])
					else:
						self.tilemap[yy][xx] = deepcopy(tl.tlist['shop'][0])
						
			self.tilemap[y][x-2] = deepcopy(tl.tlist['shop'][2])
			self.tilemap[y][x+2] = deepcopy(tl.tlist['shop'][2])
			self.tilemap[y-2][x] = deepcopy(tl.tlist['shop'][2])
			self.tilemap[y+2][x] = deepcopy(tl.tlist['shop'][2])   
			
			if self.map_type == 'orcish_mines':			
				self.npcs[y][x] = deepcopy(ml.mlist['shop'][1])
			elif self.map_type == 'grot':			
				self.npcs[y][x] = deepcopy(ml.mlist['shop'][2])
			else:
				self.npcs[y][x] = deepcopy(ml.mlist['shop'][0])#the elfish shopkeeper is only for fallback...In the elfish fortress the shops are spawned on a other way
	
	def make_monsters_angry(self,x,y,style):
		
		for yy in range(y-3,y+4):
			for xx in range(x-3,x+4):
				
				try:
					if self.npcs[yy][xx] != 0:
						if self.npcs[yy][xx].anger == style:
							lvl = self.npcs[yy][xx].lvl
							self.npcs[yy][xx] = deepcopy(ml.mlist['angry_monster'][self.npcs[yy][xx].anger_monster])
							self.set_monster_strength(xx,yy,player.pos[2],lvl)
							if player.difficulty == 4:
								self.npcs[yy][xx].AI_style = 'ignore'		
				except:
					None
	
	def time_pass(self):
		#This function refresches the map for every day that past since players last visit... make plants growing etc.
		
		if self.last_visit != time.day_total:
			
			screen.render_load(10)
			
			past_time = time.day_total - self.last_visit
			
			if past_time < 0:
				past_time = 364 - past_time
				
			for c in range (0,past_time):
				
				for y in range (0,max_map_size):
					for x in range(0,max_map_size):
						
						tile = self.tilemap[y][x]
						
						#######Life of plants######
						
						#1. Scrub
						if tile.grow_group == 'scrub':
							rand = random.randint(0,99)
							if rand < 50:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
							
						if tile.grow_group == 'scrub_buds':
							rand = random.randint(0,99)
							if rand < 90:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
						
						if tile.grow_group == 'scrub_blossom':
							rand = random.randint(0,99)
							if rand < 80:
								scrubs = random.randint(0,2)
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[scrubs][0]][tile.conected_tiles[scrubs][1]])
								self.tilemap[y][x].replace = replace
							
						if tile.grow_group == 'scrub_berries':
							rand = random.randint(0,99)
							if rand < 50:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]])
								self.tilemap[y][x].replace = replace
							elif rand > 49 and rand < 75:
								numbers =(-1,1)
								
								for yy in numbers:
									for xx in numbers:
										try:
											
											if self.tilemap[y+yy][x+xx].can_grown == True:
											
												coin = random.randint(0,99)
												
												if coin < 25: #25%
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy([tile.conected_tiles[1][0]][tile.conected_tiles[1][1]])
													self.tilemap[y+yy][x+xx].replace = replace
										except:
											None
											
						if tile.grow_group == 'scrub_scruffy':
							rand = random.randint(0,99)
							if rand < 90:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]])
								self.tilemap[y][x].replace = replace
							else:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[1][0]][tile.conected_tiles[1][1]])
								self.tilemap[y][x].replace = replace
								
						
						if tile.grow_group == 'scrub_grow':
							rand = random.randint(0,99)
							if rand < 90:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
								
						#2.Tree
						
						if tile.grow_group == 'tree_grow':
							rand = random.randint(0,99)
							if rand < 80:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
						
						if tile.grow_group == 'tree':
							rand = random.randint(0,99)
							if rand < 5:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[1][0]][tile.conected_tiles[1][1]])
								self.tilemap[y][x].replace = replace

							elif rand > 69:
								numbers =(-2,2)
								
								for yy in numbers:
									for xx in numbers:
										try:
											
											if self.tilemap[y+yy][x+xx].can_grown == True:
											
												coin = random.randint(0,3)
												
												if coin == 0:
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]])
													self.tilemap[y+yy][x+xx].replace = replace
										except:
											None
						
						#3.Herb
						
						if tile.grow_group == 'herblike':
							rand = random.randint(0,99)
							if rand < 20:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
								
						
						#4. Blue Mushrooms
						
						if tile.grow_group == 'mushroom_mud':
							
							rand = random.randint(0,99)
							
							if rand < 5:
								
								for yy in range(-1,1):
									for xx in range(-1,1):
										try:
											
											if self.tilemap[y+yy][x+xx].techID == tl.tlist['misc'][1].techID:#here is mud 
											
												cent = random.randint(0,99)
												
												if cent < 25 :
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
													self.tilemap[y+yy][x+xx].replace = replace
										except:
											None
						
						#5. Brown Mushrooms
						
						if tile.grow_group == 'mushroom_treelike':
							rand = random.randint(0,99)
							if rand < 5:
								
								for yy in range(-1,1):
									for xx in range(-1,1):
										try:
											
											if self.tilemap[y+yy][x+xx].techID == tl.tlist['global_caves'][0].techID:#here is cave ground
											
												cent = random.randint(0,99)
												
												if cent < 25 :
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]])
													self.tilemap[y+yy][x+xx].replace = replace
													
										except:
											None
							
							elif rand < 30:#make a giant mushroom
								
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[1][0]][tile.conected_tiles[1][1]])
								self.tilemap[y][x].replace = replace
									
						#6. Purple Mushrooms
						
						if tile.grow_group == 'mushroom': #let grow new mushrooms and let the old ones die(5%)
							rand = random.randint(0,99)
							if rand < 5:
								
								for yy in range(-1,1):
									for xx in range(-1,1):
										try:
											
											if self.tilemap[y+yy][x+xx].techID == tl.tlist['global_caves'][0].techID:#here is cave ground
											
												cent = random.randint(0,99)
												
												if cent < 25 :
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
													self.tilemap[y+yy][x+xx].replace = replace
												
										except:
											None
											
						#7. Agriculture
						
						if tile.grow_group == 'agri0':
							rand = random.randint(0,99)
							if rand < 50:
								if self.map_type == 'overworld': 
									self.tilemap[y][x] = tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]]
								elif self.map_type == 'cave':
									self.tilemap[y][x] = tl.tlist[tile.conected_tiles[1][0]][tile.conected_tiles[1][1]]
									
						if tile.grow_group == 'agri1': #let something grow on a acriculture (final, at the overworld) (50%)
							rand = random.randint(0,99)
							if rand < 50:
									self.tilemap[y][x] = tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]]
						
						#8. Vanish
						if tile.grow_group == 'vanish':
							rand = random.randint(0,99)
							if rand < 50:
								self.tilemap[y][x] = self.tilemap[y][x].replace
								self.containers[y][x] = 0
							
						#########add other events for growing plants etc here########
			
				self.last_visit = time.day_total #change the day of last visit to today to prevent the map of changed a second time for this day
				#if self.no_monster_respawn == False:
				#	self.spawn_monsters(player.pos[2])#spawn new monsters 
			
			for i in range(0,len(player.inventory.food)):#let the food rot in the players inventory
			
				if player.inventory.food[i] != player.inventory.nothing:
					player.inventory.food[i].rot()
			
	def exchange(self,old_tile,new_tile,use_deepcopy=False):
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				if self.tilemap[y][x].techID == old_tile.techID:
					if use_deepcopy == False:
						self.tilemap[y][x] = new_tile
					else:
						self.tilemap[y][x] = deepcopy(new_tile)
					
	def find_first(self,tile):
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				if self.tilemap[y][x].techID == tile.techID:
					return [x,y]
		
		return False
					
	def find_any(self,tile):
		
		found = []
		
		for y in range(0,max_map_size):
			for x in range(0,max_map_size):
				
				if self.tilemap[y][x].techID == tile.techID:
					found.append((x,y))
					
		if found == []:
			return False
		elif len(found) == 1:
			return found[0]
		else:
			ran = random.randint(0,len(found)-1)
			return found[ran]
	
	def find_all_moveable(self,ignore_water = True,ignore_player_pos = False):

		cordinates_list = []
		for y in range (0, max_map_size):
			for x in range (0,max_map_size):
				
				moveable = False
				
				if ignore_water == True:
					if self.tilemap[y][x].move_group == 'soil':
						moveable = True
				else:
					if self.tilemap[y][x].move_group == 'soil' or self.tilemap[y][x].move_group == 'low_liquid':
						moveable = True
				
				if ignore_player_pos == True:
					player_pos_check = False
				else:
					if (x - entrance_x < -7) or (y - entrance_y < -7) or (x - entrance_x > 7) or (y - entrance_y > 7):
						player_pos_check = False
					else:
						player_pos_check = True
				
				if (moveable == True) and (self.tilemap[y][x].damage == False) and (player_pos_check == False):
					cordinates_list.append((x,y))
						
		if len(cordinates_list) > 0:
			return cordinates_list
				
		else:
					
			return False
	
	def add_container(self, inventory, x, y, deep_copy = True):
		
		self.containers[y][x] = container(inventory,deep_copy)
	
	def make_special_monsters(self, min_no, max_no, on_tile, depth, monster_type='vase'):
		
		size = int((max_map_size*max_map_size)/(50*50))
		
		for i in range(0,size):
			
			num_monster = random.randint(min_no,max_no)
			
			if num_monster > 0:
				
				for z in range (0,num_monster):
					
					pos = self.find_any(on_tile)
					
					if monster_type == 'vase':
						
						ran = random.randint(0,99)
						
						if ran < 10:
							self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][1]) #spawn a monster vase
							self.npcs[pos[1]][pos[0]].attribute = attribute(0,0,0,0,0,1,0)
						else:
							self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][0]) #spawn a vase
							self.npcs[pos[1]][pos[0]].attribute = attribute(0,0,0,0,0,1,0)
							
					elif monster_type == 'mimic':
						
						pos = self.find_any(on_tile)
						self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][3]) #spawn a sleeping mimic
						self.npcs[pos[1]][pos[0]].attribute = attribute(0,0,0,0,0,1,0)
					
					#set monsters personal_id
					self.npcs[pos[1]][pos[0]].personal_id = str(self.npcs[pos[1]][pos[0]].techID)+'_'+str(pos[0])+'_'+str(pos[1])+'_'+str(random.randint(0,9999))
			
	def make_containers(self, min_no, max_no, on_tile, item_min, item_max, container_type='remains'):
		
		size = int((max_map_size*max_map_size)/(50*50))
		
		for i in range(0,size):
		
			num_container = random.randint(min_no,max_no)
			
			if num_container > 0:
				
				for z in range (0,num_container):
					
					place = self.find_any(on_tile)
					
					inventory = []
					
					num_items = random.randint(item_min,item_max)##############item_min,item_max
					
					for t in range (0,num_items):
					
						if container_type == 'chest':
							
							coin = random.randint(0,1)
							
							if coin == 0:#add equipmen
								classes = ['sword', 'axe', 'hammer', 'spear', 'helmet', 'armor', 'cuisse', 'shoes', 'wand', 'rune', 'rune staff', 'artefact', 'amulet', 'ring', 'talisman', 'necklace', 'pickaxe']
					
								class_num = random.randint(0,len(classes)-1)
								material = random.randint(0,20)
								plus = random.randint(-3,3)
								state = random.randint(80,100)
								
								curses = (0,1,2)
								curse_num = random.randint(0,2) 
								
								item = item_wear(classes[class_num], material, plus, state, curses[curse_num], False)
								inventory.append(item)
								
							elif coin == 1:
								items = []
								
								for i in range(14,21):
									items.append(il.ilist['misc'][i])
								for i in range(22,40):
									items.append(il.ilist['misc'][i])
								for i in range(44,47):
									items.append(il.ilist['misc'][i])
								
								for j in range(6,9):
									items.append(il.ilist['food'][j])	
								for j in range(13,25):
									items.append(il.ilist['food'][j])
								for j in range(29,32):
									items.append(il.ilist['food'][j])
									
								ran = random.randint(0,len(items)-1)
								inventory.append(deepcopy(items[ran]))
									
						elif container_type == 'remains':
						
							classes = ['sword', 'axe', 'hammer', 'spear', 'helmet', 'armor', 'cuisse', 'shoes', 'wand', 'rune', 'rune staff', 'artefact', 'amulet', 'ring', 'talisman', 'necklace', 'pickaxe']
						
							class_num = random.randint(0,len(classes)-1)
							material = random.randint(0,20)
							plus = random.randint(-3,3)
							state = random.randint(20,60)
					
							curses = (0,1,2)
							curse_num = random.randint(0,2) 
					
							item = item_wear(classes[class_num], material, plus, state, curses[curse_num], False)
							inventory.append(item)
					
					if container_type == 'chest':
					
						self.add_container(inventory, place[0], place[1])
						replace = self.tilemap[place[1]][place[0]]
						self.tilemap[place[1]][place[0]] = deepcopy(tl.tlist['functional'][4])#chest
						self.tilemap[place[1]][place[0]].replace = replace
					
					elif container_type == 'remains':
						replace_tile = self.tilemap[place[1]][place[0]]
						self.add_container(inventory, place[0], place[1])
						self.tilemap[place[1]][place[0]] = deepcopy(tl.tlist['functional'][6])#remains
						self.tilemap[place[1]][place[0]].replace = replace_tile

	def exchange_when_surrounded(self, tile_check, tile_replace, number_neighbors):
		
		#check all cordinates for their neighbors(including them self) and exchange th tile when the number of neighbors with the same techID => number_neighbors
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				count = 0
				
				for yy in range (-1,2):
					for xx in range (-1,2):
						
						try:
							if self.tilemap[y+yy][x+xx].techID == tile_check.techID or self.tilemap[y+yy][x+xx].techID == tile_replace.techID:
								count += 1
						except:
							None
							
				if count >= number_neighbors:
					self.tilemap[y][x] = tile_replace
									
	def sget(self):
		
		string = ''
		
		for c in range (0,max_map_size):
			for d in range (0,max_map_size):
				
				
				if d != player.pos[0] or c != player.pos[1]:
					
					if self.known[c][d] != 0:
						string = string + self.tilemap[c][d].char
					else:
						string += '\033[0;30;40m '
				else:
					string = string + player.char
				
			string = string + '\n'
		
		return string
		
	def set_sanctuary(self,startx,starty):
		
		for y in range (starty-2, starty+3):
			for x in range (startx-2, startx+3):
				
				self.tilemap[y][x] = deepcopy(tl.tlist['sanctuary'][0])#sanctuary floor
				
				if x == startx-2 or x == startx or x == startx+2: 
					if y == starty-2 or y == starty or y == starty+2:
						
						self.tilemap[y][x] = deepcopy(tl.tlist['sanctuary'][1])#sanctuary pilar
						
		self.tilemap[starty][startx] = deepcopy(tl.tlist['sanctuary'][2])#sanctuary spawn point
		
		self.tilemap[starty-1][startx] = deepcopy(tl.tlist['functional'][20])#divine gift
		self.tilemap[starty-1][startx].replace = tl.tlist['sanctuary'][0]
		
		material_pick = random.randint(0,10)
		material_axe = random.randint(0,10)
		material_amo = random.randint(0,10)
		amo_classes = ('shoes','cuisse','armor','helmet')
		ran = random.randint(0,3)
		amo_class = amo_classes[ran]
		
		pick = item_wear('pickaxe', material_pick,0)
		axe = item_wear('axe',material_axe,0)
		amo = item_wear(amo_class,material_amo,0)
		ran_tunica = random.randint(0,2)
		
		#original
		self.add_container([pick,axe,amo,il.ilist['misc'][3],il.ilist['misc'][2],il.ilist['misc'][51],il.ilist['clothe'][ran_tunica]],startx,starty-1)
		#/original
		
		# build demo: self.add_container([pick,axe,amo,il.ilist['misc'][3],il.ilist['misc'][16],il.ilist['misc'][22],il.ilist['misc'][23],il.ilist['clothe'][ran_tunica]],startx,starty-1)
		
		# cloth demo: self.add_container([il.ilist['clothe'][0],il.ilist['clothe'][1],il.ilist['clothe'][2],il.ilist['clothe'][3],il.ilist['clothe'][4],il.ilist['clothe'][5],il.ilist['clothe'][6],il.ilist['clothe'][7]],startx,starty-1)
		
		# magic demo: self.add_container([pick,axe,amo,il.ilist['misc'][3],il.ilist['misc'][36],il.ilist['misc'][24],il.ilist['misc'][29],il.ilist['clothe'][ran_tunica]],startx,starty-1)
		
		self.tilemap[starty+1][startx] = deepcopy(tl.tlist['functional'][1])#stair down
		self.tilemap[starty+1][startx].damage = -1
		self.tilemap[starty+1][startx].damage_mes = 'Your wounds are cured.'
		self.tilemap[starty+1][startx].build_here = False
		

		
class world_class():
	
	def __init__(self,tilelist):
		
		global max_map_size
		
		screen.render_load(0)
		
		name = save_path + os.sep + 'world.data'
		
		self.map_size = 52
		
		self.startx = 0
		self.starty = 0
		
		try:
			
			f = open(name, 'rb')
			temp = p.load(f)
			screen.render_load(1)
			self.maplist = temp.maplist
			self.map_size = temp.map_size
			max_map_size = self.map_size
			self.startx = temp.startx
			self.starty = temp.starty
			
		except:
			screen.render_load(2)
			if force_small_worlds == False:
				self.choose_size()
			self.maplist = []
		
			for x in range (0,7):
				self.maplist.append({})
				
			screen.render_load(3)
		
			pos = self.grassland_generator(0,0,30,80,5,int((max_map_size*max_map_size)/20))
			
			self.startx = pos[0]
			self.starty = pos[1]
			
			#screen.render_load(4)
			self.cave_generator(4)
			
			#screen.render_load(15)
			#self.grot_generator(3)
			
			#screen.render_load(16)
			test = False
			while test==False:
				test = self.elfish_generator(3)
			
			#screen.render_load(17)
			#self.mine_generator(9)
			
			self.border_generator(6)
			
			#screen.render_load(18)
			self.desert_generator(20)
			
			screen.render_load(5)
			
	def default_map_generator(self, name, tiles, tilelist):	#check if tilelist can be deleted
		
		tilemap = []
		
		for i in range (0,max_map_size):
			tilemap.append([])
		
		a = 0
		
		for b in range (0,max_map_size):
			
			ran_num = random.randint(0,len(tl.tlist[tiles])-1)
			tilemap[a].append(tl.tlist[tiles][ran_num])
			
		b = 0
		
		for a in range (1,max_map_size):
		
			ran_num = random.randint(0,len(tl.tlist[tiles])-1)
			tilemap[a].append(tl.tlist[tiles][ran_num])
			
		for a in range (1,max_map_size):
			for b in range (1,max_map_size):
				
				ran_same = random.randint(0,9)
				
				if ran_same < 5 :
					tilemap[a].append(tilemap[a-1][b])
				elif ran_same < 8:
					tilemap[a].append(tilemap[a][b-1])
				else:
					ran_num = random.randint(0,len(tl.tlist[tiles])-1)
					tilemap[a].append(tl.tlist[tiles][ran_num])
					
		m = maP(name ,tilemap)
		
		return m
		
	def border_generator(self,layer):
		
		cave_name = 'local_0_0'
		m = self.default_map_generator(cave_name,'global_caves', tilelist)
		m.map_type = 'border'
		
		m.fill(tl.tlist['functional'][0])#fill with border
		
		self.maplist[layer][cave_name] = m
		
	def grot_generator(self,layer):
		
		screen.render_load(15,1)
		
		cave_name = 'dungeon_0_0'
		m = self.default_map_generator(cave_name,'global_caves', tilelist)
		m.map_type = 'grot'
		m.build_type = 'None'
		
		m.fill(tl.tlist['global_caves'][3])#fill with hard rock
		m.drunken_walker(int(max_map_size/2),int(max_map_size/2),tl.tlist['misc'][0],(((max_map_size*max_map_size)/100)*40))#set low water
		
		m.set_frame(tl.tlist['functional'][0])
		
		chance_ore = layer*5
		chance_gem = layer*3
		
		screen.render_load(15,10)
			
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
					
				if m.tilemap[y][x].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
						
					replace = m.tilemap[y][x].replace
						
					coin = random.randint(0,1)
					percent = random.randint(1,100) 
						
					if coin == 0 and percent <= chance_ore:
						m.tilemap[y][x] = tl.tlist['misc'][4]#set ore here
						m.tilemap[y][x].replace = replace
					elif coin == 1 and percent <= chance_gem:
						m.tilemap[y][x] = tl.tlist['misc'][5]#set gem here
						m.tilemap[y][x].replace = replace
		
		screen.render_load(15,40)
		
		for y in range (0,max_map_size):
				for x in range (0,max_map_size):
					
					if m.tilemap[y][x].techID == tl.tlist['misc'][1].techID:#this is mud
						
						cent = random.randint(0,99)
						
						if cent < 10: #its a chance of 10% that a blue mushroom spawns here
							
							replace = m.tilemap[y][x]
							m.tilemap[y][x] = tl.tlist['misc'][6]
							m.tilemap[y][x].replace = replace
							
							m.containers[y][x] = container([deepcopy(il.ilist['food'][1])])
		
		screen.render_load(15,75)
		
		num_lilys = int(((max_map_size*max_map_size)/100)*3)
		
		for i in range (0,num_lilys):
			pos = m.find_any(tl.tlist['misc'][0])#find low wather
			try:
				coin = random.randint(0,1)
				if coin == 0:
					m.tilemap[pos[1]][pos[0]] = tl.tlist['misc'][10]#set a water lily
				else:
					m.tilemap[pos[1]][pos[0]] = tl.tlist['misc'][14]#set a water lily with blossom
					
			except:
				None
		
		screen.render_load(15,90)
		
		pos = m.find_any(tl.tlist['misc'][0])#find any low water tile
		m.tilemap[pos[1]][pos[0]] = tl.tlist['dungeon'][15]#set stair up
		entrance_x = pos[0]
		entrance_y = pos[1]
		
		for sy in range(pos[1]-4,pos[1]+5):
			for sx in range(pos[0]-4,pos[0]+5):
				try:
					if m.tilemap[sy][sx].move_group == 'soil':
						m.tilemap[sy][sx] = deepcopy(m.tilemap[sy][sx])
						m.tilemap[sy][sx].move_group == 'dry_entrance'
					elif m.tilemap[sy][sx].move_group == 'low_liquid':
						m.tilemap[sy][sx] = deepcopy(m.tilemap[sy][sx])
						m.tilemap[sy][sx].move_group == 'wet_entrance'
				except:
					None
		
		m.make_shops()
		
		m.spawn_monsters(3)
		
		screen.render_load(15,99)
							
		self.maplist[layer][cave_name] = m
		
	def elfish_generator(self,layer):
		
		screen.render_load(16,40)
		
		map_name = 'local_0_0'
		m = self.default_map_generator(map_name,'global_caves', tilelist)
		m.map_type = 'elfish_fortress'
		m.no_monster_respawn = True
		
		m.fill(tl.tlist['elfish'][0])
		
		for y in range (10, max_map_size-10,10):
				
			ran = random.randint(0,3)
			for yy in range (y-1,y+2):
				if ran < 3:
					m.imp_connect((0,max_map_size-1),(yy,yy),tl.tlist['elfish'][1],tl.tlist['elfish'][1],tl.tlist['elfish'][1])
					
			if ran < 3:
				m.imp_connect((0,max_map_size-1),(y-2,y-2),tl.tlist['elfish'][3],tl.tlist['elfish'][1],tl.tlist['elfish'][1])
				m.imp_connect((0,max_map_size-1),(y+2,y+2),tl.tlist['elfish'][3],tl.tlist['elfish'][1],tl.tlist['elfish'][1])
		
		screen.render_load(16,45)
				
		for x in range (10, max_map_size-10,10):
			
			ran = random.randint(0,3)
			for xx in range (x-1,x+2):
				if ran < 3:
					m.imp_connect((xx,xx),(0,max_map_size-1),tl.tlist['elfish'][1],tl.tlist['elfish'][1],tl.tlist['elfish'][1])
		
			if ran < 3:
				m.imp_connect((x-2,x-2),(0,max_map_size-1),tl.tlist['elfish'][3],tl.tlist['elfish'][1],tl.tlist['elfish'][1])
				m.imp_connect((x+2,x+2),(0,max_map_size-1),tl.tlist['elfish'][3],tl.tlist['elfish'][1],tl.tlist['elfish'][1])
		
		m.cut(5,max_map_size-6,5,max_map_size-6,tl.tlist['elfish'][3])
		
		building_count = 0
		run = True
		
		screen.render_load(16,50)
		
		while run:
			
			pos=m.find_first(tl.tlist['elfish'][0])
			
			if pos != False:
				m.floating(pos[0],pos[1],tl.tlist['elfish'][5],tl.tlist['elfish'][3])#fill with help passive
				building_count += 1
			else:
				run = False
				
		m.exchange(tl.tlist['elfish'][5],tl.tlist['elfish'][0])
		
		screen.render_load(16,55)
				
		if building_count < 6:
			return False #return false to make a loop if there are to less buildings inside the map
		
		num_temples = int((float(building_count)/100)*10)
		
		if num_temples == 0:
			num_temples = 1
			
		num_agriculture = int((float(building_count)/100)*10)
		
		if num_agriculture == 0:
			num_agriculture=1
		
		num_meetingarea = int((float(building_count)/100)*10)
		
		if num_meetingarea == 0:
			num_meetingarea = 1
			
		num_marketplace = int((float(building_count)/100)*10)
		
		if num_marketplace == 0:
			num_marketplace = 1
		
		num_libaries = int((float(building_count)/100)*10)
		
		if num_libaries == 0:
			num_libaries = 1
			
		num_dwellings = building_count-num_temples-num_agriculture-num_meetingarea-num_marketplace-num_libaries
		
		screen.render_load(16,60)
			
		m.cut(5,max_map_size-6,5,max_map_size-6,tl.tlist['elfish'][1])
		
		for i in range(0,num_agriculture):
			pos = m.find_any(tl.tlist['elfish'][0])#find any elfish_floor_indoor
			m.floating(pos[0],pos[1],tl.tlist['elfish'][2],tl.tlist['elfish'][1])#replace this building with elfish_agriculture
		
		for y in range(0,max_map_size,2):
			for x in range(0,max_map_size):
				
				if m.tilemap[y][x].techID == tl.tlist['elfish'][2].techID:#this is elfish agriculture
					m.tilemap[y][x] = tl.tlist['misc'][0]#set low water
		
		screen.render_load(16,61)
		
		m.cut(5,max_map_size-6,5,max_map_size-6,tl.tlist['elfish'][3])	
		
		for i in range(0,num_marketplace):#set marketplaces
			pos = m.find_any(tl.tlist['elfish'][0])#find any elfish_floor_indoor
			m.floating(pos[0],pos[1],tl.tlist['elfish'][4],tl.tlist['elfish'][3])#fill this building with elfish_active
			pos = m.find_first(tl.tlist['elfish'][4])
			size = m.get_quarter_size(pos[0],pos[1])
			
			for y in range(pos[1]+1,pos[1]+size[1]-1,2):
				for x in range(pos[0]+1,pos[0]+size[0]-1,3):
					m.npcs[y][x] = ml.mlist['shop'][0]
			
			m.exchange(tl.tlist['elfish'][4],tl.tlist['shop'][0])
		
		screen.render_load(16,62)
		
		for i in range(0,num_temples):
			
			pos = m.find_any(tl.tlist['elfish'][0])#find any elfish_floor_indoor
			m.floating(pos[0],pos[1],tl.tlist['elfish'][4],tl.tlist['elfish'][3])#fill this building with elfish_active
			pos = m.find_first(tl.tlist['elfish'][4])
			size = m.get_quarter_size(pos[0],pos[1])
			
			for y in range(pos[1],pos[1]+size[1],2):
				for x in range(pos[0],pos[0]+size[0],2):
					m.tilemap[y][x] = deepcopy(tl.tlist['functional'][22])
					m.tilemap[y][x].replace = tl.tlist['elfish'][0]
					m.tilemap[y][x].civilisation = False
			
			m.tilemap[pos[1]+int(size[1]/2)][pos[0]+int(size[0]/2)] = deepcopy(tl.tlist['functional'][15])#set a altar
			m.tilemap[pos[1]+int(size[1]/2)][pos[0]+int(size[0]/2)].replace = tl.tlist['elfish'][0]
			m.tilemap[pos[1]+int(size[1]/2)][pos[0]+int(size[0]/2)].civilisation = False
			
			m.exchange(tl.tlist['elfish'][4],tl.tlist['elfish'][5])
		
		screen.render_load(16,63)
		
		for i in range(0,num_meetingarea):
			
			pos = m.find_any(tl.tlist['elfish'][0])
			m.floating(pos[0],pos[1],tl.tlist['elfish'][4],tl.tlist['elfish'][3])#fill this building with elfish_active
			pos = m.find_first(tl.tlist['elfish'][4])
			size = m.get_quarter_size(pos[0],pos[1])
			
			for y in range(pos[1]+2,pos[1]+size[1]-2):
				for x in range(pos[0]+2,pos[0]+size[0]-1,4):
					m.tilemap[y][x] = deepcopy(tl.tlist['functional'][16]) #set table
					m.tilemap[y][x].replace = tl.tlist['elfish'][0]
					m.tilemap[y][x].civilisation = False
					
					for xx in range(x-1,x+2):
						if m.tilemap[y][xx].techID == tl.tlist['elfish'][4].techID:
							m.tilemap[y][xx] = deepcopy(tl.tlist['functional'][18])
							m.tilemap[y][xx].replace = tl.tlist['elfish'][0]
							m.tilemap[y][xx].civilisation = False
			
					for yy in range(y-1,y+2):
						if m.tilemap[yy][x].techID == tl.tlist['elfish'][4].techID:
							m.tilemap[yy][x] = deepcopy(tl.tlist['functional'][18])
							m.tilemap[yy][x].replace = tl.tlist['elfish'][0]
							m.tilemap[yy][x].civilisation = False
			
			m.exchange(tl.tlist['elfish'][4],tl.tlist['elfish'][5])
		
		screen.render_load(16,64)
			
		for i in range(0,num_libaries):
			
			pos = m.find_any(tl.tlist['elfish'][0])
			m.floating(pos[0],pos[1],tl.tlist['elfish'][4],tl.tlist['elfish'][3])#fill this building with elfish_active
			pos = m.find_first(tl.tlist['elfish'][4])
			size = m.get_quarter_size(pos[0],pos[1])
			
			for y in range(pos[1]+1,pos[1]+size[1]-1,2):
				for x in range(pos[0]+1,pos[0]+size[0]-1,2):
					
					m.tilemap[y][x] = deepcopy(tl.tlist['functional'][19])
					m.tilemap[y][x].civilisation = False
			
			m.exchange(tl.tlist['elfish'][4],tl.tlist['elfish'][5])
		
		screen.render_load(16,65)
		
		for i in range(0,num_dwellings):
			
			pos = m.find_any(tl.tlist['elfish'][0])
			m.floating(pos[0],pos[1],tl.tlist['elfish'][4],tl.tlist['elfish'][3])#fill this building with elfish_active
			pos = m.find_first(tl.tlist['elfish'][4])
			pos_original = pos
			size = m.get_quarter_size(pos[0],pos[1])
			
			num_beds = int((size[0]*size[1])/9)
			num_furniture = int((size[0]*size[1])/25)
			
			for y in range(pos[1],pos[1]+size[1]):
				for x in range(pos[0],pos[0]+size[0]):
					m.tilemap[y][x] = tl.tlist['elfish'][5]
			
			for y in range(pos[1]+1,pos[1]+size[1]-1):
				for x in range(pos[0]+1,pos[0]+size[0]-1):
					m.tilemap[y][x] = tl.tlist['elfish'][4]
					
			for i in range(0,num_beds):#set beds
				pos = m.find_any(tl.tlist['elfish'][4])
				m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['functional'][8])
				m.tilemap[pos[1]][pos[0]].replace = deepcopy(tl.tlist['building'][9])
				m.tilemap[pos[1]][pos[0]].civilisation = False
				m.tilemap[pos[1]][pos[0]].replace.civilisation = False
			
			for i in range(0,num_furniture):#set furnaces
				pos = m.find_any(tl.tlist['elfish'][4])
				m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['functional'][14])
				m.tilemap[pos[1]][pos[0]].replace = deepcopy(tl.tlist['building'][9])
				m.tilemap[pos[1]][pos[0]].civilisation = False
				m.tilemap[pos[1]][pos[0]].replace.civilisation = False
				
			for i in range(0,num_furniture):#set wb's
				pos = m.find_any(tl.tlist['elfish'][4])
				ran = random.randint(9,13)
				m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['functional'][ran])
				m.tilemap[pos[1]][pos[0]].replace = deepcopy(tl.tlist['building'][9])
				m.tilemap[pos[1]][pos[0]].civilisation = False
				m.tilemap[pos[1]][pos[0]].replace.civilisation = False
				
			for y in range(pos_original[1]+1,pos_original[1]+size[1]-1):#set blue floor
				for x in range(pos_original[0]+1,pos_original[0]+size[0]-1):
					if m.tilemap[y][x].techID == tl.tlist['elfish'][4].techID:
						 m.tilemap[y][x] = deepcopy(tl.tlist['building'][9])
						 m.tilemap[y][x].civilisation = False
		
		screen.render_load(16,66)
						
		for yy in range(0,max_map_size,5):
			for xx in range(0,max_map_size):
				if m.tilemap[yy][xx].techID == tl.tlist['elfish'][3].techID:#this is elfish wall
					m.tilemap[yy][xx] = deepcopy(tl.tlist['building'][2]) #set a open door here
					m.tilemap[yy][xx].civilisation = False
					
					for yyy in range(yy-1,yy+2):
						for xxx in range(xx-1,xx+2):
							if yyy >= 0 and xxx >= 0 and xxx < max_map_size and yyy < max_map_size:
								if m.tilemap[yyy][xxx].techID != tl.tlist['elfish'][0].techID and m.tilemap[yyy][xxx].techID != tl.tlist['elfish'][1].techID and m.tilemap[yyy][xxx].techID != tl.tlist['shop'][0].techID and m.tilemap[yyy][xxx].techID != tl.tlist['building'][2].techID and m.tilemap[yyy][xxx].techID != tl.tlist['elfish'][3].techID and m.tilemap[yyy][xxx].techID != tl.tlist['elfish'][2].techID and m.tilemap[yyy][xxx].techID != tl.tlist['misc'][0].techID:
									#if a field next to a door isn't elfish_indoor, elfish_wall or shop_floor set it to elfish_indoor
									m.tilemap[yyy][xxx] = tl.tlist['elfish'][0]
		
		screen.render_load(16,67)
		
		for yy in range(0,max_map_size):
			for xx in range(0,max_map_size,5):
				if m.tilemap[yy][xx].techID == tl.tlist['elfish'][3].techID:#this is elfish wall
					m.tilemap[yy][xx] = deepcopy(tl.tlist['building'][2]) #set a open door here
					m.tilemap[yy][xx].civilisation = False
					
					for yyy in range(yy-1,yy+2):
						for xxx in range(xx-1,xx+2):
							if yyy >= 0 and xxx >= 0 and xxx < max_map_size and yyy < max_map_size:
								if m.tilemap[yyy][xxx].techID != tl.tlist['elfish'][0].techID and m.tilemap[yyy][xxx].techID != tl.tlist['elfish'][1].techID and m.tilemap[yyy][xxx].techID != tl.tlist['shop'][0].techID and m.tilemap[yyy][xxx].techID != tl.tlist['building'][2].techID and m.tilemap[yyy][xxx].techID != tl.tlist['elfish'][3].techID and m.tilemap[yyy][xxx].techID != tl.tlist['elfish'][2].techID and m.tilemap[yyy][xxx].techID != tl.tlist['misc'][0].techID:
									#if a field next to a door isn't elfish_indoor, elfish_wall or shop_floor set it to elfish_indoor
									m.tilemap[yyy][xxx] = tl.tlist['elfish'][0]
		
		screen.render_load(16,68)
		
		m.cut(5,max_map_size-6,5,max_map_size-6,tl.tlist['elfish'][3])
		m.set_frame(tl.tlist['functional'][0])
		
		#set fontains
		
		for y in range(10,max_map_size-10,10):
			for x in range(10,max_map_size-10,10):
				
				if m.tilemap[y][x].techID == tl.tlist['elfish'][1].techID:
					
					coin = random.randint(0,1)
					
					if coin == 0:
						m.tilemap[y][x] = deepcopy(tl.tlist['functional'][7])#set a fontain
						m.tilemap[y][x].replace = tl.tlist['elfish'][1]
						m.tilemap[y][x].civilisation = False #this is no players fontain 
		
		m.exchange(tl.tlist['elfish'][5],tl.tlist['elfish'][0])
		m.spawn_monsters(6)
		
		self.maplist[layer][map_name] = m
		
		screen.render_load(16,69)
		
	def mine_generator(self,layer):
		
		screen.render_load(17,1)
		
		cave_name = 'dungeon_0_0'
		m = self.default_map_generator(cave_name,'global_caves', tilelist)
		m.map_type = 'orcish_mines'
		m.build_type = 'None'
		
		screen.render_load(17,10)
		
		m.fill(tl.tlist['mine'][1])#fill with mine wall
		screen.render_load(17,30)
		m.drunken_walker(int(max_map_size/2),int(max_map_size/2),tl.tlist['mine'][0],((max_map_size**2/100)*45))
		screen.render_load(17,50)
		
		screen.render_load(17,60)
		
		m.exchange_when_surrounded(tl.tlist['mine'][1],tl.tlist['global_caves'][3],8) #only the outer tiles become mine wall
		
		screen.render_load(17,70)
		
		for y in range (0, max_map_size):
			for x in range(0,max_map_size):
				 
				if m.tilemap[y][x].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
				 
					ran = random.randint(0,99)
					 
					if ran > 69:
						 
						 m.tilemap[y][x] = tl.tlist['misc'][4]#set ore
						 m.tilemap[y][x].replace = tl.tlist['global_caves'][0]
					
					elif ran < 10:
						m.tilemap[y][x] = tl.tlist['misc'][5]#set gem
						m.tilemap[y][x].replace = tl.tlist['global_caves'][0]
		
		screen.render_load(17,80)
		
		m.set_frame(tl.tlist['functional'][0])
		
		m.make_shops()
		
		m.make_containers(15,30,tl.tlist['mine'][0],1,4,'remains')
		
		num_moss = int(((max_map_size*max_map_size)/100)*3)
		
		for i in range (0,num_moss):
			pos = m.find_any(tl.tlist['mine'][0])#find mine floor
			try:
				m.tilemap[pos[1]][pos[0]] = tl.tlist['mine'][2]#set blood moss
			except:
				None
		
		screen.render_load(17,90)
		
		pos = m.find_any(tl.tlist['mine'][0])#find any mine floor tile
		m.tilemap[pos[1]][pos[0]] = tl.tlist['dungeon'][17]#set stair up
		entrance_x = pos[0]
		entrance_y = pos[1]
		
		for sy in range(pos[1]-4,pos[1]+5):
			for sx in range(pos[0]-4,pos[0]+5):
				try:
					if m.tilemap[sy][sx].move_group == 'soil':
						m.tilemap[sy][sx] = deepcopy(m.tilemap[sy][sx])
						m.tilemap[sy][sx].move_group == 'dry_entrance'
					elif m.tilemap[sy][sx].move_group == 'low_liquid':
						m.tilemap[sy][sx] = deepcopy(m.tilemap[sy][sx])
						m.tilemap[sy][sx].move_group == 'wet_entrance'
				except:
					None
		
		m.spawn_monsters(9)
		
		screen.render_load(17,99)
							
		self.maplist[layer][cave_name] = m
		
	def cave_generator(self, deep):
			
		cave_name = 'local_0_0'
		
		p = 9
				
		for d in range(1,deep+2):
			
			screen.render_load(4,p+(d*5))
			
			m = self.default_map_generator(cave_name,'global_caves', tilelist)
			if d < 4:
				m.map_type = 'cave'
			else:
				m.map_type = 'lava_cave'
				m.thirst_multi_day = 2
				m.thirst_multi_night = 2
			
			if d > 3:
				m.exchange(tl.tlist['global_caves'][4],tl.tlist['misc'][2])#exchange lava against hot cave ground
				if d > 4:
					m.exchange_when_surrounded(tl.tlist['misc'][2],tl.tlist['global_caves'][4],8)#make lava spots between hot cave ground
					num = int((max_map_size*max_map_size)/(50*50))
					for i in range(0,num):
						ran = random.randint(0,1)
						if ran > 0:
							pos = m.find_any(tl.tlist['global_caves'][0]) #cave ground
							m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['functional'][23])# make master forges
			else:
				m.exchange(tl.tlist['global_caves'][4],tl.tlist['misc'][1])#exchange lava against mud
				m.exchange_when_surrounded(tl.tlist['misc'][1],tl.tlist['misc'][0],8)#make low water spots between mud
				
			#######set mushrooms, ore and gems
		
			chance_ore = d
			chance_gem = d/2
			
			for y in range (0,max_map_size):
				for x in range (0,max_map_size):
					
					if m.tilemap[y][x].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
						
						replace = m.tilemap[y][x].replace
						
						coin = random.randint(0,1)
						percent = random.randint(1,100) 
						
						if coin == 0 and percent <= chance_ore:
							m.tilemap[y][x] = tl.tlist['misc'][4]#set ore here
							m.tilemap[y][x].replace = replace
						elif coin == 1 and percent <= chance_gem:
							m.tilemap[y][x] = tl.tlist['misc'][5]#set gem here
							m.tilemap[y][x].replace = replace
							
					if m.tilemap[y][x].techID == tl.tlist['misc'][1].techID:#this is mud
						
						cent = random.randint(0,99)
						
						if cent < 10: #its a chance of 10% that a blue mushroom spawns here
							
							replace = m.tilemap[y][x]
							m.tilemap[y][x] = tl.tlist['misc'][6]
							m.tilemap[y][x].replace = replace
					
					if m.tilemap[y][x].techID == tl.tlist['global_caves'][0].techID:#this is cave ground
						
						cent = random.randint(0,99)
						
						if cent < 10: #its a chance of 10% that a brown mushroom spawns here
							
							replace = m.tilemap[y][x]
							m.tilemap[y][x] = tl.tlist['misc'][7]
							m.tilemap[y][x].replace = replace
							
						elif cent < 15: #its a chance of 5% that a purple mushroom spawns here
							
							replace = m.tilemap[y][x]
							m.tilemap[y][x] = tl.tlist['misc'][8]
							m.tilemap[y][x].replace = replace
			
			m.set_frame(tl.tlist['functional'][0])
			
			if d == 1:#set stair up on lvl 1
				pos = (int(max_map_size/2),int(max_map_size/2))
				m.tilemap[pos[1]+1][pos[0]] = deepcopy(tl.tlist['functional'][2])#stair down
				m.tilemap[pos[1]+1][pos[0]].damage = -1
				m.tilemap[pos[1]+1][pos[0]].damage_mes = 'Your wounds are cured.'
				m.tilemap[pos[1]+1][pos[0]].build_here = False
				
				for x in range(0,max_map_size):
					if m.tilemap[x][pos[0]].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
						ran = random.randint(1,2)
						m.tilemap[x][pos[0]] = deepcopy(tl.tlist['global_caves'][ran])
						
				for y in range(0,max_map_size):
					if m.tilemap[pos[1]+1][y].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
						ran = random.randint(1,2)
						m.tilemap[pos[1]+1][y] = deepcopy(tl.tlist['global_caves'][ran])
			
			#set grot/mine at lvl 1 and 4
			
			if d == 1:
				ran_pos = m.find_any(tl.tlist['global_caves'][0])
				m.tilemap[ran_pos[1]][ran_pos[0]] = tl.tlist['dungeon'][14]
			
			if d == 4:
				ran_pos = m.find_any(tl.tlist['global_caves'][0])
				m.tilemap[ran_pos[1]][ran_pos[0]] = tl.tlist['dungeon'][16]
			
			m.make_containers(1,2,tl.tlist['global_caves'][0],2,5,'chest')#set some chests
			m.make_special_monsters(0,1,tl.tlist['global_caves'][0],d,'mimic')#maybe set some mimics
			m.make_special_monsters(15,25,tl.tlist['global_caves'][0],d,'vase')#set some vases
			
			m.spawn_monsters(d)
							
			self.maplist[d][cave_name] = m
							
	def grassland_generator(self,x,y,chance_scrubs, chance_trees, chance_herbs, number_rocks):
		# chance_scrubs and chance_trees must be between 0 and 99
		
		screen.render_load(3,1)
		name = 'local_0_0'
		
		helpmap = self.default_map_generator('1','help',tilelist)
		
		tilemap = []
		for a in range (0,max_map_size):
			tilemap.append([])
			for b in range (0,max_map_size):
				tilemap[a].append(0)
	
		m = maP(name,tilemap)
		m.map_type = 'overworld'
		
		screen.render_load(3,2)
		
		m.fill(tl.tlist['local'][0])#fill the map with grass
				
		# set scrubs
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				if helpmap.tilemap[y][x].techID == tl.tlist['help'][0].techID: #<---scrub here
					chance = random.randint(0,99)
					if chance < chance_scrubs:
						scrubs = (1,3,4,6,7,8,9)
						coin = random.randint(0,len(scrubs)-1)
						m.tilemap[y][x] = deepcopy(tl.tlist['local'][scrubs[coin]])
						m.tilemap[y][x].replace = tl.tlist['local'][0]
						
		screen.render_load(3,3)
							
		#set trees
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				if helpmap.tilemap[y][x].techID == tl.tlist['help'][1].techID: #<---tree here
					chance = random.randint(0,99)
					if chance < chance_trees:
						coin = random.randint(10,13)
						m.tilemap[y][x] = tl.tlist['local'][coin]
						m.tilemap[y][x].replace = tl.tlist['local'][0]#grass
		
		screen.render_load(3,4)
		
		#set herbs
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				if helpmap.tilemap[y][x].techID == tl.tlist['help'][0].techID: #<---scrub here
					chance = random.randint(0,99)
					if chance < chance_herbs:
						coin = random.randint(15,16)
						m.tilemap[y][x] = tl.tlist['local'][coin]
						m.tilemap[y][x].replace = tl.tlist['local'][0]#grass
		
		screen.render_load(3,5)
			
		# set rocks
		
		for n in range (0,number_rocks):
			x = random.randint(0,max_map_size-1)
			y = random.randint(0,max_map_size-1)
			m.tilemap[y][x] = tl.tlist['local'][14]
			m.tilemap[y][x].replace = tl.tlist['local'][0]#grass
		
		screen.render_load(3,6)
		
		#set water
			
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				if helpmap.tilemap[y][x].techID == tl.tlist['help'][2].techID: #<---water here
					m.tilemap[y][x] = tl.tlist['misc'][0] # set low water here
		
		screen.render_load(3,7)
					
		m.exchange_when_surrounded(tl.tlist['misc'][0],tl.tlist['misc'][3],8) # exchange low wather against deep water
		
		pos = (int(max_map_size/2),int(max_map_size/2))
		
		m.set_sanctuary(pos[0],pos[1])
		
		m.set_frame(tl.tlist['functional'][0])
		
		screen.render_load(3,8)
		
		#set guidepost
		y = max_map_size -2
		x = random.randint(2,max_map_size-2)
		m.tilemap[y][x] = tl.tlist['extra'][6]
		m.tilemap[y][x].replace = tl.tlist['local'][0]#grass
		m.tilemap[y-1][x] = tl.tlist['local'][0]#grass
		
		#set dungeon
		ran_pos = m.find_any(tl.tlist['local'][0])
		m.tilemap[ran_pos[1]][ran_pos[0]] = tl.tlist['dungeon'][7]
		
		m.spawn_monsters(0)
					
		self.maplist[0][name] = m
		
		screen.render_load(3,9)
		
		return pos
	
	def tutorial_generator(self):
 		
 		#0: Basic initializing
 		
 		screen.render_load(19,0)
 		
 		name = 'dungeon_0_0'
 		
 		tilemap = []
 		for a in range (0,max_map_size):
 			tilemap.append([])
 			for b in range (0,max_map_size):
 				tilemap[a].append(0)
 		
 		m = maP(name,tilemap)
 		m.map_type = 'dungeon'
 		m.build_type = 'None'
 		m.monster_plus = 0
 		m.monster_num = 0
 		
 		m.fill(tl.tlist['tutorial'][1])
 		
 		screen.render_load(19,10)
 		
 		#1: Room one
 		for y in range(5,10):
 			for x in range(5,10):
 				m.tilemap[y][x] = tl.tlist['tutorial'][0]
 				
 		for y in range(10,13):
 			m.tilemap[y][7] = tl.tlist['tutorial'][0]
 			
 		for y in range(13,18):
 			for x in range(5,10):
 				m.tilemap[y][x] = tl.tlist['tutorial'][0]
 				
 		m.countdowns.append(countdown('init_tutorial',0,0,0))
 		self.maplist[0][name] = m
	
	def dungeon_generator(self,monster_plus,stair_down=True,num_traps=10,style='Dungeon'):#possible other style = 'Tomb'
		
		#0: Basic initializing
		
		screen.render_load(19,0)#Render progress bar 0%
		
		if style == 'Tomb':								#Set the graphics
			tl.tlist['dungeon'][1].tile_pos = (4,6)		#
			tl.tlist['dungeon'][6].tile_pos = (4,7)		#Sandstone walls,hidden doors and corridors for the acient tomb
			tl.tlist['dungeon'][9].tile_pos = (4,7)		#
		else:											#
			tl.tlist['dungeon'][1].tile_pos = (10,6)	#
			tl.tlist['dungeon'][6].tile_pos = (2,6)		#Default walls,hidden doors and corridors for the default dungeon
			tl.tlist['dungeon'][9].tile_pos = (2,6)		#
		
		name = 'dungeon_0_0'#map name
		
		tilemap = []							#Initializing a empty tilemap
		for a in range (0,max_map_size):		#
			tilemap.append([])					#
			for b in range (0,max_map_size):	#
				tilemap[a].append(0)			#
		
		m = maP(name,tilemap)					#Generate a Map-object
		if style == 'Tomb':						#
			m.map_type = 'tomb'					#
		else:									#
			m.map_type = 'dungeon'				#and set a few constants for the new map
		m.build_type = 'None'					#
		m.monster_plus = monster_plus			#
		m.monster_num = 0.3						#
		m.no_monster_respawn = True				#
		
		m.fill(tl.tlist['dungeon'][9])#fill the map with dungeon wall tiles
		
		screen.render_load(19,10)#Render progress bar 10%
		
		#1: Set rooms
			#Important fact: No matter how big the mapsize is set, 
			#dundeons only use the 52x52 tiles in the upper left connor.
			#Thats as big as a small map.
		test_build = True								#Seperate the dungeon in a 3x3 grit.
		while test_build:								#Every part of the grit has a 66% chance to be a room
			parts_with_rooms = []						#
														#
			for part_y in range(0,3):					#
				for part_x in range(0,3):				#
					ran = random.randint(0,9)			#
					if ran > 3:							#
						pick = (part_x,part_y)			#
						parts_with_rooms.append(pick)	#
			
			if len(parts_with_rooms) > 5:	#every dungeon level needs at least 5 rooms
				test_build = False			#
			
		coord_x = []						#transform the coordinates from the 3x3 grit into
		coord_y = []						#real coordinates on the tilemap(center of the rooms)
											#
		for c in parts_with_rooms:			#
			x_offset = random.randint(0,5)	#
			y_offset = random.randint(0,5)	#
											#
			real_x = 9+(15*c[0])+x_offset	#
			real_y = 9+(15*c[1])+y_offset	#
											#
			coord_x.append(real_x)			#
			coord_y.append(real_y)			#
		
		m.imp_connect(coord_x,coord_y,tl.tlist['dungeon'][1],tl.tlist['dungeon'][0],tl.tlist['dungeon'][0])#connect the room cooardinathe with corridor
			
		for i in range(0,len(coord_x)-1):#set variable roome size for all rooms
			x_minus = random.randint(2,4)#
			x_plus = random.randint(3,5) #
			y_minus = random.randint(2,4)#
			y_plus = random.randint(3,5) #
				
			for yy in range(coord_y[i]-y_minus-1,coord_y[i]+y_plus+1):			#draw walls around the rooms
				for xx in range(coord_x[i]-x_minus-1,coord_x[i]+x_plus+1):		#
					m.tilemap[yy][xx] = tl.tlist['dungeon'][9]					#
																				
			for yy in range(coord_y[i]-y_minus,coord_y[i]+y_plus):				#draw the room floor
				for xx in range(coord_x[i]-x_minus,coord_x[i]+x_plus):			#
					m.tilemap[yy][xx] = tl.tlist['dungeon'][0]					#
		
		screen.render_load(19,25) #progress bar 25%
			
		#2: Set doors			
						
		for yyy in range(0,52):
			for xxx in range(0,52):			#the 52 is hard scripted to safe performance
					
				if m.tilemap[yyy][xxx].techID == tl.tlist['dungeon'][9].techID:										#Set all tiles that are surrounded by two moveable tiles on two opponent sides as doors 
					if m.tilemap[yyy-1][xxx].move_group == 'soil' and m.tilemap[yyy+1][xxx].move_group == 'soil':	#
						m.tilemap[yyy][xxx] = tl.tlist['dungeon'][3]												#
					elif m.tilemap[yyy][xxx-1].move_group == 'soil' and m.tilemap[yyy][xxx+1].move_group == 'soil':	#
						m.tilemap[yyy][xxx] = tl.tlist['dungeon'][3]												#
				
		for yyy in range(0,52):
			for xxx in range(0,52):			#the 52 is hard scripted to safe performance
				
				if m.tilemap[yyy][xxx].techID == tl.tlist['dungeon'][3].techID:	#Remove all doors that are next to another door.
					size = m.get_quarter_size(xxx,yyy)							#Only spare one door per wall
					if size[0] > 1:												#
						for rx in range(xxx,xxx+size[0]+1):						#
							m.tilemap[yyy][rx] = tl.tlist['dungeon'][9]			#
						rrx = int(xxx+((rx-xxx)/2))								#
						m.tilemap[yyy][rrx] = tl.tlist['dungeon'][3]			#
																				#
						if m.tilemap[yyy-1][rrx].move_group != 'soil':			#
							m.tilemap[yyy-1][rrx] = tl.tlist['dungeon'][1]		#
						if m.tilemap[yyy+1][rrx].move_group != 'soil':			#
							m.tilemap[yyy+1][rrx] = tl.tlist['dungeon'][1]		#
																				#
					if size[1] > 1:												#
						for ry in range(yyy,yyy+size[1]+1):						#
							m.tilemap[ry][xxx] = tl.tlist['dungeon'][9]			#
						rry = int(yyy+((ry-yyy)/2))								#
						m.tilemap[rry][xxx] = tl.tlist['dungeon'][3]			#
																				#
						if m.tilemap[rry][xxx-1].move_group != 'soil':			#
							m.tilemap[rry][xxx-1] = tl.tlist['dungeon'][1]		#
						if m.tilemap[rry][xxx+1].move_group != 'soil':			#
							m.tilemap[rry][xxx+1] = tl.tlist['dungeon'][1]		#
		
		screen.render_load(19,40)#Render progress bar 40%
		
		test = deepcopy(m)														#Make a copy of the map as is
		pos = test.find_first(tl.tlist['dungeon'][0])							#and performe a float test,
		test.floating(pos[0],pos[1],tl.tlist['misc'][0],tl.tlist['dungeon'][9])	#in order to find not conected parts.
		
		screen.render_load(19,50) #Render progress bar 50%
		
		for yyy in range(0,52):																														#Remove not connected parts
			for xxx in range(0,52):																													#
				if test.tilemap[yyy][xxx].techID != tl.tlist['dungeon'][9].techID and test.tilemap[yyy][xxx].techID != tl.tlist['misc'][0].techID:	#
					m.tilemap[yyy][xxx] = tl.tlist['dungeon'][9]																					#
		
		screen.render_load(19,60)#Render progress bar 60%
		
		for yyy in range(0,52):														#Randomize doors:
			for xxx in range(0,52):													#-normal door
																					#-resisting door
				if m.tilemap[yyy][xxx].techID == tl.tlist['dungeon'][3].techID:		#-etc.
					ran = random.randint(3,6)										#
					m.tilemap[yyy][xxx] = tl.tlist['dungeon'][ran]					#
					
		
		screen.render_load(19,70)#Render progress bar 70%
						
		#3: Make stairs
		stair_up_pos = m.find_any(tl.tlist['dungeon'][0])							#Set a up leading stair on any floor tile.
		entrance_x = stair_up_pos[0]
		entrance_y = stair_up_pos[1]
		if style == 'Tomb':															#
			m.tilemap[stair_up_pos[1]][stair_up_pos[0]] = tl.tlist['dungeon'][19]	#
		else:																		#
			m.tilemap[stair_up_pos[1]][stair_up_pos[0]] = tl.tlist['dungeon'][8]	#
			
		for sy in range(stair_up_pos[1]-4,stair_up_pos[1]+5):
			for sx in range(stair_up_pos[0]-4,stair_up_pos[0]+5):
				try:
					if m.tilemap[sy][sx].move_group == 'soil':
						m.tilemap[sy][sx] = deepcopy(m.tilemap[sy][sx])
						m.tilemap[sy][sx].move_group = 'dry_entrance'
					elif m.tilemap[sy][sx].move_group == 'low_liquid':
						m.tilemap[sy][sx] = deepcopy(m.tilemap[sy][sx])
						m.tilemap[sy][sx].move_group = 'wet_entrance'
				except:
					None
			
		if stair_down == True:																#If we are not on the deepest lvl:
			stair_down_pos = m.find_any(tl.tlist['dungeon'][0])								#Set a down leading stair on any floor tile.
			if style == 'Tomb':																#
				m.tilemap[stair_down_pos[1]][stair_down_pos[0]] = tl.tlist['dungeon'][18]	#
			else:																			#
				m.tilemap[stair_down_pos[1]][stair_down_pos[0]] = tl.tlist['dungeon'][7]	#
		else: 																		#Make a chest whit a reward on the deepest lvl instead
			chest_pos = m.find_any(tl.tlist['dungeon'][0])							#
			m.tilemap[chest_pos[1]][chest_pos[0]] = tl.tlist['dungeon'][20]			#
			m.tilemap[chest_pos[1]][chest_pos[0]].replace = tl.tlist['dungeon'][0]	#
			
			if style == 'Tomb':
				m.add_container([il.ilist['clothe'][3],il.ilist['misc'][33],il.ilist['misc'][40]],chest_pos[0],chest_pos[1])# set the interior of the chest
			else:																											#
				m.add_container([il.ilist['clothe'][4],il.ilist['misc'][33],il.ilist['misc'][41]],chest_pos[0],chest_pos[1])#
		
		screen.render_load(19,80)#Render progress bar 80%
		
		#4: Make Traps
		
		for i in range(0,num_traps):										#Set hidden traps on random floor tiles.
			pos = m.find_any(tl.tlist['dungeon'][0])						#
			replace = m.tilemap[pos[1]][pos[0]]								#
			m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['dungeon'][10])	#Traps have to be deepcopied to work proper.
			m.tilemap[pos[1]][pos[0]].replace = replace						#
		
		screen.render_load(19,90) #Render Progress bar 90%
		#5: Make interior
		num_rooms = len(parts_with_rooms)														#Make chests with random loot
		m.make_containers(int(num_rooms/3),int(num_rooms/2),tl.tlist['dungeon'][0],1,3,'chest')	#
		
		for c in range(0,num_rooms):						#Set random fontains on floor tiles
			pos = m.find_any(tl.tlist['dungeon'][0])		#
			ran = random.randint(0,99)						#
			if ran < 15:									#
				tile = deepcopy(tl.tlist['dungeon'][12])	#acid fontain
			elif ran > 84:									#
				tile = deepcopy(tl.tlist['dungeon'][13])	#healing fontain
			else:											#
				tile = deepcopy(tl.tlist['functional'][7])	#fontain
				tile.civilisation = False					#
				tile.build_here = False						#
				tile.can_grown = False						#
			tile.replace = tl.tlist['dungeon'][0]			#
			m.tilemap[pos[1]][pos[0]] = tile				#
			
		coin = random.randint(0,1)						#Set a Altar on 50% of all maps
		if coin == 1:									#that are generated with this function
			pos = m.find_any(tl.tlist['dungeon'][0])	#
			tile = deepcopy(tl.tlist['functional'][15])	#
			tile.civilisation = False					#
			tile.build_here = False						#
			tile.can_grown = False						#
			tile.replace = tl.tlist['dungeon'][0]		#
			m.tilemap[pos[1]][pos[0]] = tile			#
			
		m.spawn_monsters(0)															#Spawn initial monsters
		m.make_special_monsters(10,20,tl.tlist['dungeon'][0],m.monster_plus,'vase')	#
		m.make_special_monsters(1,2,tl.tlist['dungeon'][0],m.monster_plus,'mimic')	#
			
		self.maplist[1][name] = m # Add map to world.maplist
		
		screen.render_load(19,99) #Render progress bar 99%
		
	def desert_generator(self,chance_object):
		#chance_objects must be between 0 and 99
		
		screen.render_load(18,70)
		
		name = 'desert_0_0'
		
		tilemap = []
		for a in range (0,max_map_size):
			tilemap.append([])
			for b in range (0,max_map_size):
				tilemap[a].append(0)
	
		m = maP(name,tilemap)
		m.map_type = 'desert'
		m.build_type = 'Part'
		m.thirst_multi_day = 2
		
		m.fill(tl.tlist['extra'][0])
		
		y_river = random.randint((17),(max_map_size-17))
		river_offset = random.randint(-3,3)
		plus = 0
		minus = 0
		
		screen.render_load(18,71)
		
		for c in range (0,max_map_size):
			
			for g in range (-2,7):
				m.tilemap[y_river+river_offset+g][c] = tl.tlist['local'][0]#set grass
				
			for w in range (0,5):
				m.tilemap[y_river+river_offset+w][c] = tl.tlist['misc'][0]#set low water
				
			if river_offset < 4:
				plus = 1
			else:
				plus = 0
				
			if river_offset > -4:
				minus = -1
			else:
				minus = 0
				
			offset_change = random.randint(minus,plus)
			river_offset += offset_change
			
		m.exchange_when_surrounded(tl.tlist['misc'][0],tl.tlist['misc'][3],7)
		
		screen.render_load(18,72)
		
		for b in range(2,max_map_size-2,10):
			
			#north side of the river
			building_offset =random.randint(0,4)
			number_beds = 0
			
			for y in range(y_river-12,y_river-7):
				for x in range(b+building_offset,b+building_offset+5):
					
					if x == b+building_offset or x == b+building_offset+4:
						if y == y_river-10:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][9])
						else:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][2])
					elif y == y_river-12 or y == y_river-8:
						if x == b+building_offset+2:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][9])
						else:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][2])
					else:
						m.tilemap[y][x] = deepcopy(tl.tlist['extra'][1])
						
					if x == b+building_offset+1 or x == b+building_offset+3:
						if y == y_river-11 or y == y_river-9:
							
							obj_here = random.randint(0,2) #0: nothing, 1:bed 2:workbench
							
							if number_beds == 0:
								obj_here = 1
								
							if obj_here != 0:
								if obj_here == 1:
									obj = ('functional',8)
									number_beds += 1
								else:
									ran = random.randint(9,15)
									obj = ('functional',ran)
								
								m.tilemap[y][x] = deepcopy(tl.tlist[obj[0]][obj[1]])
								m.tilemap[y][x].replace = deepcopy(tl.tlist['extra'][1])
								m.tilemap[y][x].civilisation = False
								m.tilemap[y][x].build_here = False
								m.tilemap[y][x].move_group = 'house'
							
			#south side of the river			
			building_offset =random.randint(0,4)
			number_beds = 0
			
			screen.render_load(18,73)
			
			for y in range(y_river+8,y_river+13):
				for x in range(b+building_offset,b+building_offset+5):
					
					if x == b+building_offset or x == b+building_offset+4:
						if y == y_river+10:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][9])
						else:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][2])
					elif y == y_river+12 or y == y_river+8:
						if x == b+building_offset+2:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][9])
						else:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][2])
					else:
						m.tilemap[y][x] = deepcopy(tl.tlist['extra'][1])
		
					if x == b+building_offset+1 or x == b+building_offset+3:
						if y == y_river+9 or y == y_river+11:
							
							obj_here = random.randint(0,2) #0: nothing, 1:bed 2:workbench
							
							if number_beds == 0:
								obj_here = 1
								
							if obj_here != 0:
								if obj_here == 1:
									obj = ('functional',8)
									number_beds += 1
								else:
									ran = random.randint(9,15)
									obj = ('functional',ran)
								
								m.tilemap[y][x] = deepcopy(tl.tlist[obj[0]][obj[1]])
								m.tilemap[y][x].replace = deepcopy(tl.tlist['extra'][1])
								m.tilemap[y][x].civilisation = False
								m.tilemap[y][x].build_here = False
								m.tilemap[y][x].move_group = 'house'
		
		make_bridges = True
		num_bridges = 0
		num_bridges_max = ((max_map_size/50)*3)+1
		
		screen.render_load(18,74)
		
		while num_bridges < num_bridges_max:
			x_pos = random.randint(5,max_map_size-5)
				
			num_wall = 0
				
			for test in range(0,max_map_size):
				if m.tilemap[test][x_pos].techID == tl.tlist['extra'][2].techID:
					num_wall += 1
				
			if num_wall == 0:
				num_bridges += 1
				for y in range(0,max_map_size):
					if m.tilemap[y][x_pos].techID == tl.tlist['misc'][0].techID or m.tilemap[y][x_pos].techID == tl.tlist['misc'][3].techID: #this is low wather or deep water
						replace = deepcopy(m.tilemap[y][x_pos])
						m.tilemap[y][x_pos] = deepcopy(tl.tlist['extra'][8])
						m.tilemap[y][x_pos].replace = replace
				
		for y in range (0,max_map_size):
			for x in range (0,max_map_size): 
				if m.tilemap[y][x].techID == tl.tlist['extra'][0].techID:
					chance = random.randint(0,99)
					if chance < chance_object:
						obj_numbers = (3,4,5,14)
						coin = random.randint(0,len(obj_numbers)-1)
						m.tilemap[y][x] = tl.tlist['extra'][obj_numbers[coin]]
						m.tilemap[y][x].replace = tl.tlist['extra'][0]#sand
				elif m.tilemap[y][x].techID == tl.tlist['local'][0].techID:
					chance = random.randint(0,99)
					if chance < chance_object:
						coin = random.randint(10,13)
						m.tilemap[y][x] = tl.tlist['extra'][coin]
						m.tilemap[y][x].replace = tl.tlist['local'][0]#grass
				elif m.tilemap[y][x].techID == tl.tlist['extra'][9].techID:
					for yy in range(y-1,y+2):
						if m.tilemap[yy][x].replace != None:
							m.tilemap[yy][x] = m.tilemap[yy][x].replace
					for xx in range(x-1,x+2):
						if m.tilemap[y][xx].replace != None:
							m.tilemap[y][xx] = m.tilemap[y][xx].replace
						
				if m.tilemap[y][x].techID == tl.tlist['functional'][8].techID:#bed
					ran = random.randint(5,6)
					m.npcs[y][x] = deepcopy(ml.mlist['special'][ran])
					m.set_monster_strength(x,y,0)
					
		
		m.set_frame(tl.tlist['functional'][0])
		
		screen.render_load(18,75)
		
		#set guidepost
		y = 2
		x = random.randint(2,max_map_size-2)
		m.tilemap[y][x] = tl.tlist['extra'][7]
		m.tilemap[y][x].replace = tl.tlist['extra'][0]#sand
		m.tilemap[y+1][x] = tl.tlist['extra'][0]#sand
		
		#set tomb
		ran_pos = m.find_any(tl.tlist['extra'][0])
		m.tilemap[ran_pos[1]][ran_pos[0]] = tl.tlist['dungeon'][18]
		
		m.spawn_monsters(0)
					
		self.maplist[0][name] = m
		
	def choose_size(self):
		#this is a all in one function with render, choose and set
		global max_map_size # I know its no good style
		run = True
		mms = 52 #this is a temp variable that is used to store the worth for the max_map_size till this function is called 
		num = 0
		
		while run:
		#Part 1: Render
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))

			s.blit(bg,(0,0))

			text = '~Choose Map-Size~ [Press ['+key_name['e']+'] to choose]'
			text_image = screen.font.render(text,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			entries = ('Small (50x50)', 'Medium (100x100)', 'Big (150x150)')
			messages = ('Everything on a very small space.', 'Perfect size for the most players.', 'A big world.')
			mapsizes = (52,102,152)
			
			for i in range (0,3):
				
				entry_image = screen.font.render(entries[i],1,(0,0,0))
				if low_res == False:
					s.blit(entry_image,(21,150+i*30))#blit menu_items
				else:
					s.blit(entry_image,(21,66+i*25))#blit menu_items
				
			if low_res == False:
				s.blit(gra_files.gdic['display'][4],(0,145+num*30))#blit marker
			else:
				s.blit(gra_files.gdic['display'][4],(0,58+num*25))#blit marker
				
			entry_image = screen.font.render(messages[num],1,(255,255,255))
			if low_res == True:
				s.blit(entry_image,(2,225))
			else:
				s.blit(entry_image,(5,335))
			
			if game_options.mousepad == 1 and low_res == False:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			
			screen.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
		#Step 2: Choose
		
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
		
			if ui == 'w':
			
				num -= 1
				if num < 0:
					num = 2
				
			if ui == 's':
			
				num += 1
				if num > 2:
					num = 0
				
			if ui == 'e':
			
				mms = mapsizes[num]
				max_map_size = mms
				self.map_size = mms
				run = False
			
class mob():
	
	def __init__(self, name, on_map, attribute, pos =[40,40,0],glob_pos=[0,0],build='Manual'):
		
		self.name = name
		self.on_map = on_map
		self.attribute = attribute
		self.lp = attribute.max_lp
		self.mp = attribute.max_mp
		self.pos = pos	
		self.glob_pos = glob_pos
		self.last_map = 'Foo'
		self.cur_map = 'Bar'
		self.cur_z = self.pos[2]
		self.last_z = 'Baz'
		
	def move(self, x=0, y=0):
		
		mc = self.move_check(x,y)
		tile_move_group = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group
		player_move_groups = ['soil','low_liquid','holy','shop','house','wet_entrance','dry_entrance']
		
		swim_check = True
		
		for i in ('Head','Body','Legs','Feet'):
			if player.inventory.wearing[i] != player.inventory.nothing:
				swim_check = False
				
		if swim_check == True:
			player_move_groups.append('swim')
		
		if self.buffs.immobilized > 0:
			player_move_groups = ['not_existent_group1','not_existent_group2']
		
		move_check2 = False	
		
		for j in player_move_groups:
			if j == tile_move_group:
				move_check2 = True
		
		if mc == True:
			if x > 0 and move_check2 == True and self.pos[0] < max_map_size - 1:
				self.pos[0] += 1
			
			if x < 0 and move_check2 == True and self.pos[0] > 0:
				self.pos[0] -= 1
			
			if y > 0 and move_check2 == True and self.pos[1] < max_map_size - 1:
				self.pos[1] += 1
			
			if y < 0 and move_check2 == True and self.pos[1] > 0:
				self.pos[1] -= 1
				
		self.stand_check()
		
	def move_check(self,x,y):
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'door':
			if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['dungeon'][4].techID or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['dungeon'][5].techID or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['dungeon'][6].techID:
				#this is a resisting door or a hidden door
				sfx.play('locked')
			else:
				sfx.play('open')	
			message.add(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_mes)
			world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace
			return False
		
		try:
			
			if world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]+y][self.pos[0]+x] != 0:
				player.attack_monster(self.pos[0]+x,self.pos[1]+y)
				return False
			
			if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].destroy != False: #for digging
				
				if self.attribute.pickaxe_power + player.inventory.wearing['Pickaxe'].attribute.pickaxe_power >= world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].destroy:
					if self == player:
						message.add(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_mes)
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID != tl.tlist['building'][3].techID: #this isn't a door
							sfx.play('break')
						
						try:
							material = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_resources[0]
							mat_num = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_resources[1]
							mes = player.inventory.materials.add(material,mat_num)
							message.add(mes)
						except:
							None
							
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['building'][3].techID: #this is a closed door
							world.maplist[self.pos[2]][self.on_map].countdowns.append(countdown('door', self.pos[0]+x, self.pos[1]+y,3))
							sfx.play('open')
							
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace)
					
					if player.inventory.wearing['Pickaxe'] != player.inventory.nothing and world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID != tl.tlist['building'][3].techID:
					
						player.inventory.wearing['Pickaxe'].take_damage()
					
						if player.inventory.wearing['Pickaxe'].state > 0:
							player.inventory.wearing['Pickaxe'].set_name()
						else:
							message.add('Your tool breaks into pieces.')
							player.inventory.wearing['Pickaxe'] = player.inventory.nothing
							sfx.play('item_break')
					
				else:
					if self == player:
							message.add('You are unable to destroy this with the tool in your hand.')
					
				return False
			
			else:
				None
				
			if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'tree':
				
				if player.inventory.wearing['Axe'] != player.inventory.nothing: #if player has a axe in his hand			
					chop_success = True
					player.inventory.wearing['Axe'].take_damage()
					
					if player.inventory.wearing['Axe'].state > 0:
						player.inventory.wearing['Axe'].set_name()
					else:
						message.add('Your axe breaks into pieces.')
						player.inventory.wearing['Axe'] = player.inventory.nothing
						sfx.play('item_break')
					
				else:
					message.add('That hurts!')
					player.lp -= 1
					sfx.play('hit')
					if random.randint(0,9) != 0: #90% to fail chopping down the wood with bare hands
						chop_success = False
					else:
						chop_success = True
				
				if chop_success == True:
					material = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_resources[0]
					mat_num = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_resources[1]
					mes = player.inventory.materials.add(material,mat_num)
					message.add(mes)
					sfx.play('chop')
					world.maplist[self.pos[2]][self.on_map].make_monsters_angry(self.pos[0],self.pos[1],'tree')
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace) #let the tree disappear
				return False
						
					
			if self.buffs.immobilized == 0:
				if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'low_liquid' or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'swim' or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'wet_entrance':
					sfx.play('walk_wet')
				else:
					sfx.play('walk_dry')
			else:
				sfx.play('immobilized')
			
			return True
			
		except:
			
			None
			
	def stand_check(self):
		
		if self.on_map != self.cur_map:
			self.last_map = self.cur_map
			self.cur_map = self.on_map
		 	
		if self.pos[2] != self.cur_z:
			self.last_z = self.cur_z
			self.cur_z = self.pos[2]
		
		radius = 5
		
		if player.pos[2] > 0:
			radius = 2
		elif player.pos[2] == 0:
			if time.hour > 22 or time.hour < 4:
				radius = 2 
			elif time.hour > 21 or time.hour < 5:
				radius = 3 
			elif time.hour > 20 or time.hour < 6:
				radius = 4 
			elif time.hour > 19 or time.hour < 7:
				radius = 5 
			
		if player.buffs.light > 0:
			radius = 5
			
		if player.buffs.blind > 0:
			radius = 1
		
		message.add(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].move_mes,True)
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage > 0:
			self.lp = self.lp - world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage
			if self == player:
				try:
					message.add(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage_mes + ' (' + str(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage) + ' Damage)')
				except:
					None
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage < 0:
			if self.lp < self.attribute.max_lp:	
				self.lp = self.lp - world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage
		
		luck = player.attribute.luck + player.inventory.wearing['Neck'].attribute.luck
		
		for y in range(player.pos[1]-1,player.pos[1]+2):
			for x in range(player.pos[0]-1,player.pos[0]+2):
				if world.maplist[self.pos[2]][self.on_map].tilemap[y][x].techID == tl.tlist['dungeon'][6].techID:#this is a secret door
					ran = random.randint(0,25)#check players luck
					if ran < luck:
						world.maplist[self.pos[2]][self.on_map].tilemap[y][x] = tl.tlist['dungeon'][3]
						message.add('You notice a hidden door.')
				
				if world.maplist[self.pos[2]][self.on_map].tilemap[y][x].techID == tl.tlist['dungeon'][10].techID:#this is a trap
					ran = random.randint(0,25)#check players luck
					if ran < luck:
						world.maplist[self.pos[2]][self.on_map].tilemap[y][x].tile_pos = (10,8)
						message.add('You notice a trap.')
				
		for y in range (-radius,radius+1):#line of sight
			for x in range (-radius,radius+1):
				try:
				
					dist = ((x)**2+(y)**2)**0.5
				
					if dist <= radius+1 or dist >= radius-1:
						
						run = True
						c = 0
						
						while run:
						
							try:
								yy = ((y*c)/dist)
							except:
								yy = 1
						
							try:
								xx = ((x*c)/dist)
							except:
								xx = 1
							
							view_x = int(xx) + self.pos[0]
							view_y = int(yy) + self.pos[1]
							
							world.maplist[self.pos[2]][self.on_map].known[view_y][view_x] = 1
							
							
							if world.maplist[self.pos[2]][self.on_map].tilemap[view_y][view_x].transparency == True and c < radius:
								c+=1
							else:
								run = False
				except:
					None
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['dungeon'][10].techID:
			
			kind =random.randint(0,3)
			position = deepcopy(player.pos)#coppy player pos before the trap is triggered because teleport traps could change it
			
			if kind == 0:#dart trap
				ran = random.randint(0,25)
				
				if ran < luck:
					screen.write_hit_matrix(player.pos[0],player.pos[1],3)
					message.add('A flying dagger miss you.')
					sfx.play('miss')
				else:
					player.lp -= 3
					screen.write_hit_matrix(player.pos[0],player.pos[1],4)
					message.add('A flying dagger hits you.')
					sfx.play('hit')
					
					
			elif kind == 1:#teleport trap
				t=world.maplist[self.pos[2]][self.on_map].find_all_moveable()
				ran = random.randint(0,len(t)-1)
				player.pos[0] = t[ran][0]
				player.pos[1] = t[ran][1]
				message.add('You are teleported randomly.')
				player.stand_check()
				
			elif kind == 2:#blinding trap
				ran = random.randint(10,30)
				player.buffs.set_buff('blind',ran)
				message.add('A garish flash blinds you.')
				
			elif kind == 3:#magic trap
				player.mp = 0
				screen.write_hit_matrix(player.pos[0],player.pos[1],7)
				message.add('You loose your focus.')
				
			replace = world.maplist[self.pos[2]][self.on_map].tilemap[position[1]][position[0]].replace
			world.maplist[self.pos[2]][self.on_map].tilemap[position[1]][position[0]] = deepcopy(tl.tlist['dungeon'][11])
			world.maplist[self.pos[2]][self.on_map].tilemap[position[1]][position[0]].replace = replace
					
		if player.lp <= 0:
			screen.render_dead()
		
		bgm.check_for_song()
					
	def enter(self):
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'stair_down':
			if world.maplist[self.pos[2]+1][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['functional'][2].techID: #if there is a stair up below this
				player.pos[2] += 1
				player.stand_check()#to unveil the surroundings
			else:
				message.add('This stair seem to be blocked.')
			
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'stair_up': #this is a stair up
			if world.maplist[self.pos[2]-1][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['functional'][1].techID: #if there is a stair down above
				player.pos[2] -= 1
				player.stand_check()#to unveil the surroundings
			else:
				message.add('This stair seem to be blocked.')
			
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'drink':#this is a low wather or a fontain
			#drink water
			if player.attribute.thirst < player.attribute.thirst_max:
				message.add('You take a sip of water.')
				player.attribute.thirst += 240 #this is 1/3 of the water te player needs per day
				if player.attribute.thirst > player.attribute.thirst_max:
					player.attribute.thirst = player.attribute.thirst_max+1#the +1 is because the player will lose one point at the same round so you would get just 99%
			else:
				message.add('You are not thirsty right now.')
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'drink_acid':#this is a acid fontain
			#drink acid water
			if player.attribute.thirst < player.attribute.thirst_max:
				message.add('You take a sip of water.')
				player.lp -= 5
				message.add('It hurts like acid.')
				replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(tl.tlist['functional'][7])
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].civilisation = False
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].build_here = False
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].can_grown = False
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
			else:
				message.add('You are not thirsty right now.')
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'drink_heal':#this is a healing fontain
			#drink healing water
			if player.attribute.thirst < player.attribute.thirst_max:
				message.add('You take a sip of water.')
				if player.lp < player.attribute.max_lp:
					player.lp += 5
					if player.lp > player.attribute.max_lp:
						player.lp = player.attribute.max_lp
						message.add('Your wounds are cured.')
				
				replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(tl.tlist['functional'][7])
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].civilisation = False
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].build_here = False
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].can_grown = False
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
			else:
				message.add('You are not thirsty right now.')
				
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'resource':
			res = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_resources[0]
			num = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_resources[1]
			try:
				conected_tile = (world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[0],world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[1])
			except:
				None
			test = player.inventory.materials.add(res,num)
			if test != 'Full!':
				message.add(test)
				replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				try:
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(tl.tlist[conected_tile[0]][conected_tile[1]])
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
				except:
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = replace
			else:
				message.add(test)
				
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'sleep':#this is a bed
			#sleep a bit
			sleep = True
			lp = player.lp
			
			while sleep:
				screen.render_load(12)
				time.tick()
				player.attribute.tiredness += 5
				if player.buffs.adrenalised_max > 0:
					player.buffs.adrenalised_max -= 5
				
				if player.buffs.adrenalised_max < 0:
					player.buffs.adrenalised_max = 0
				
				if player.lp < lp:
					message.add('You were hurt!')
					sleep = False
				
				if player.attribute.tiredness >= player.attribute.tiredness_max:#wake up because you've slept enough
					player.attribute.tiredness = player.attribute.tiredness_max +1 #the +1 is because the player will lose one point at the same round so you would get just 99%
					message.add('You feel refreshed.')
					sleep = False
					
				if int((player.attribute.hunger_max*100)/player.attribute.hunger) < 11:
					message.add('You feel hungry.')
					sleep = False
					
				if int((player.attribute.thirst_max*100)/player.attribute.thirst) < 11:
					message.add('You feel thirsty.')
					sleep = False
					
				monster_test = False
					
				for y in range (player.pos[1]-1, player.pos[1]+2):#check for a monster
					for x in range (player.pos[0]-1, player.pos[0]+2):
						
						try:
							if world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]][self.pos[0]] != 0:#<-------change this so that friendly npcs are ignored 
								monster_test = True	
						except:
							None
						
				if monster_test == True:#wake up because a monster borders the players sleep
					message.add('You wake up with a sense of danger.')
					sleep = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'gather':
			help_container = container([world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_items])
			item_name = help_container.items[0].name
			test_loot = help_container.loot(0)
			if test_loot == True:
				string = '+[' + item_name + ']'
				message.add(string)
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = 0
			else:
				message.add('Your inventory is full!')
				
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'gather_scrub':
			help_container = container([world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_items])
			item_name = help_container.items[0].name
			test_loot = help_container.loot(0)
			if test_loot == True:
				string = 'You take ' + item_name + '.'
				message.add(string)
				cat = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[2][0]
				num = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[2][1]
				replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = tl.tlist[cat][num]
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
			else:
				message.add('Your inventory is full!')
				
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'carpenter': 
			#this is a carpenter's workbench
			
			run = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request('['+key_name['e']+'] - produce something (-10 Wood)', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave')
					else:
						screen.render_request('['+key_name['e']+'] -     XXXXXXXXXXXX            ', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave')
				else:
					screen.render_request('['+key_name['e']+'] - produce something (-10 Wood)', '['+key_name['b']+'] -      XXXXXXXXXXXX   ', '['+key_name['x']+'] - leave')
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					
					if test == True:
						
						if player.inventory.materials.wood >= 10:
							gc = screen.get_choice('What do you want to produce?', ('Carpenter\'s Workbench', 'Carver\'s Workbench', 'Stonecuter\'s Workbench', 'Forger\'s Workbench', 'Alchemist\'s Workshop', 'Furniture'),True)
							
							if gc < 5:# give the chosen workbench to the player
								items = (il.ilist['misc'][3],il.ilist['misc'][4],il.ilist['misc'][5],il.ilist['misc'][6],il.ilist['misc'][7])
								choose = gc
							elif gc == 5:
								items = (il.ilist['misc'][1], il.ilist['misc'][2],il.ilist['misc'][10],il.ilist['misc'][11],il.ilist['misc'][13])
								#chest, bed, table, w. seat, bookshelf
								choose = random.randint(0, len(items)-1)
							try:
								if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
									world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
								else:
									world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
									
								message_string = 'You produced a ' + items[choose].name + '.'
								message.add(message_string)
								player.inventory.materials.wood -= 10
							except:
								None
								
							run = False
						
						else:
							message.add('You have not enough wood!')
							run = False
						
				elif ui == 'b' and world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
				
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
						
				elif ui == 'x':
					
					run = False
					
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'carver': 
			#this is a carvers's workbench
			
			run = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request('['+key_name['e']+'] - produce something (-5 Wood)', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave')
					else:
						screen.render_request('['+key_name['e']+'] -     XXXXXXXXXXXX            ', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave')
				else:
					screen.render_request('['+key_name['e']+'] - produce something (-5 Wood)', '['+key_name['b']+'] -      XXXXXXXXXXXX   ', '['+key_name['x']+'] - leave')
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					
					if test == True:
						if player.inventory.materials.wood >= 5:
							
							final_choice = 'Foo'
							gc = screen.get_choice('What do you want to prodcuce exactly?', ('Tool', 'Weapon', 'Armor','Jewelry'), True)
							
							if gc == 0: #make a tool
								items = (il.ilist['misc'][14], il.ilist['misc'][44], item_wear('axe',0,0), item_wear('pickaxe',0,0))
								final_choice = screen.get_choice('What do you want to prodcuce exactly?', ('Fishing rod','Torch','Axe','Pickaxe'),True)
							elif gc == 1: #make a weapon
								items = (item_wear('spear',0,0), item_wear('sword',0,0), item_wear('hammer',0,0), item_wear('rune',0,0), item_wear('wand',0,0), item_wear('rune staff',0,0), item_wear('artefact',0,0))
								class_choice = screen.get_choice('What do you want to prodcuce?', ('Melee Weapon','Magic Weapon'), True)
								if class_choice == 0:
									final_choice = random.randint(0,2)
								else:
									final_choice = random.randint(3,6)
							elif gc == 2: #make some armor
								items = (item_wear('shoes',0,0), item_wear('cuisse',0,0), item_wear('helmet',0,0), item_wear('armor',0,0))
								final_choice = screen.get_choice('What do you want to prodcuce?', ('Shoes','Cuisse','Helmet','Armor'), True)
							elif gc == 3:#make some jewlry
								items = (item_wear('ring',0,0),  item_wear('amulet',0,0),  item_wear('necklace',0,0), item_wear('talisman',0,0))
								final_choice = screen.get_choice('What do you want to prodcuce?', ('Ring','Amulet','Necklace','Talisman'), True)
							
							choose = final_choice
							try:
								if choose != 'Foo':
									if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
									else:
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
								
								message_string = 'You produced a ' + items[choose].name + '.'
								message.add(message_string)
								if choose != 'Foo':
									player.inventory.materials.wood -= 5
							except:
								None
								
							run = False
						
						else:
							message.add('You have not enough wood!')
							run = False
						
				elif ui == 'b' and world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
				
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
						
				elif ui == 'x':
					
					run = False
									
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'stonecutter': 
			#this is a stonecutter's workbench
			
			run = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request('['+key_name['e']+'] - produce something (-10 Stone)', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave')
					else:
						screen.render_request('['+key_name['e']+'] -     XXXXXXXXXXXX            ', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave')
				else:
					screen.render_request('['+key_name['e']+'] - produce something (-10 Stone)', '['+key_name['b']+'] -      XXXXXXXXXXXX   ', '['+key_name['x']+'] - leave')
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					
					if test == True:
						if player.inventory.materials.stone >= 10:
							
							gc = screen.get_choice('What do you want to produce?' ,('Functional Things', 'Decorative Things'), True)
							
							if gc == 0: #make something functional
								items = (il.ilist['misc'][0], il.ilist['misc'][8], il.ilist['misc'][9])
								#items: fontain, furnace, altar
							else:#make something decorative
								items = (il.ilist['misc'][12],il.ilist['misc'][21])
								#items: stone seat, pilar ---> have to become more
							
							choose = random.randint(0, len(items)-1)
							try:
								if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
									world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
								else:
									world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
								
								message_string = 'You produced a ' + items[choose].name + '.'
								message.add(message_string)
								player.inventory.materials.stone -= 10
							except:
								None
								
							run = False
						
						else:
							message.add('You have not enough Stone!')
							run = False
						
				elif ui == 'b' and world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
				
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
						
				elif ui == 'x':
					
					run = False
					
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'forger' or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'masterforge': 
			#this is a forger's workbench or a master forge
			
			run = True
			
			while run:
				
				price = 5
				if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['functional'][23].techID: #this is a master forge
					price = 15
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						string = ('['+key_name['e']+'] - produce something (-' + str(price) + ' Ore)', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave')
						screen.render_request(string[0],string[1],string[2])
					else:
						screen.render_request('['+key_name['e']+'] -     XXXXXXXXXXXX            ', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave')
				else:
					string = '['+key_name['e']+'] - produce something (-' + str(price) + ' Ore)', '['+key_name['b']+'] -      XXXXXXXXXXXX   ', '['+key_name['x']+'] - leave'
					screen.render_request(string[0],string[1],string[2])
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					
					if test == True:
						if player.inventory.materials.ore >= price:
							
							material = random.randint(6,20)#tin to magnicum
							if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['functional'][23].techID: #this is a master forge
								material = 20 #magnicum only
							
							final_choice = 'Foo'
							gc = screen.get_choice('What do you want to procuce?', ('Tool', 'Weapon', 'Armor','Jewelry'), True)
							
							if gc == 0: #make a tool
								final_choice = screen.get_choice('What do you want to procuce exactly?', ('Axe', 'Pickaxe'), True)
								items = (item_wear('axe',material,0), item_wear('pickaxe',material,0)) 
							elif gc == 1: #make a weapon
								items = (item_wear('spear',material,0), item_wear('sword',material,0), item_wear('hammer',material,0), item_wear('wand',material,0), item_wear('rune',material,0), item_wear('rune staff',material,0), item_wear('artefact',material,0))
								class_choice = screen.get_choice('What do you want to prodcuce?', ('Melee Weapon','Magic Weapon'), True)
								if class_choice == 0:
									final_choice = random.randint(0,2)
								else:
									final_choice = random.randint(3,6)
							elif gc == 2: #make some armor
								final_choice = screen.get_choice('What do you want to procuce exactly?', ('Shoes', 'Cuisse', 'Helmet', 'Armor'), True)
								items = (item_wear('shoes',material,0), item_wear('cuisse',material,0), item_wear('helmet',material,0), item_wear('armor',material,0))
							elif gc == 3:#make some  jewelry
								items = (item_wear('ring',material,0),  item_wear('amulet',material,0),  item_wear('necklace',material,0), item_wear('talisman',material,0))
								final_choice = screen.get_choice('What do you want to prodcuce?', ('Ring','Amulet','Necklace','Talisman'), True)
							
							choose = final_choice
							try:
								if choose != 'Foo':
									if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
									else:
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
								
								message_string = 'You produced a ' + items[choose].name + '.'
								message.add(message_string)
								if choose != 'Foo':
									player.inventory.materials.ore -= price
							except:
								None
								
							run = False
						
						else:
							message.add('You have not enough ore!')
							run = False
						
				elif ui == 'b' and world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
				
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
						
				elif ui == 'x':
					
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'alchemist': 
			#this is a alchemists's workshop
			
			run = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request('['+key_name['e']+'] - brew a potion (-5 Herbs)', '['+key_name['b']+'] - take a potion', '['+key_name['x']+'] - leave')
					else:
						screen.render_request('['+key_name['e']+'] -     XXXXXXXXXXXX            ', '['+key_name['b']+'] - take a potion', '['+key_name['x']+'] - leave')
				else:
					screen.render_request('['+key_name['e']+'] - brew a potion (-5 Herbs)', '['+key_name['b']+'] -      XXXXXXXXXXXX   ', '['+key_name['x']+'] - leave')
				
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					
					if test == True:
						if player.inventory.materials.herb >= 5:
							
							ordenary_potions = (il.ilist['food'][13],il.ilist['food'][14],il.ilist['food'][15],il.ilist['food'][16])
							#ordenary potions are: p.o. healing, p.o. feeding, p.o. refreshing, p.o. vitalising 
							strong_potions = (il.ilist['food'][17],il.ilist['food'][18],il.ilist['food'][19],il.ilist['food'][20])
							#strong potions are: s.p.o. healing, s.p.o. feeding, s.p.o. refreshing, s.p.o. vitalising 
							upgrade_potions = (il.ilist['food'][21],il.ilist['food'][22],il.ilist['food'][23],il.ilist['food'][24])
							#upgrade potions are: p.o. hunger, p.o. thirst, p.o. tiredness, p.o. life
							
							choose = random.randint(0,99) 
							
							if choose < 70: #make a ordenary potion(70%)
								items = ordenary_potions
							elif choose < 95:#make a strong potion(25%) 
								items = strong_potions
							else:#make a upgrade potion(5%)
								items = upgrade_potions
					
							choose = random.randint(0, len(items)-1)
							
							if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
								world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
							else:
								world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
								
							message_string = 'You brewed a ' + items[choose].name + '.'
							message.add(message_string)
							player.inventory.materials.herb -= 5
							run = False
						
						else:
							message.add('You have not enough herbs!')
							run = False
						
				elif ui == 'b' and world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
				
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
						
				elif ui == 'x':
					
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'furnace': 
			#this is a furnace
			
			run = True
			
			while run:
				
				screen.render_request('['+key_name['e']+'] - fire up the furnace (-10 wood)', ' ', '['+key_name['x']+'] - leave')
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					
					if player.inventory.materials. wood >= 10:
						
						message.add('You ligth up a fire.')
						
						for i in range (0,len(player.inventory.food)):
							if player.inventory.food[i] != player.inventory.nothing: 
								if player.inventory.food[i].techID == il.ilist['food'][4].techID: #this is a fish
									message.add('You grill a fish.')
									player.inventory.food[i] = deepcopy(il.ilist['food'][5])#turn a fish into a grilled fish
								elif player.inventory.food[i].techID == il.ilist['food'][6].techID: #this are crops
									message.add('You bake a bread.')
									player.inventory.food[i] = deepcopy(il.ilist['food'][7])#turn crops into bread
								elif player.inventory.food[i].techID == il.ilist['food'][7].techID: #this is a bread
									message.add('You bake a bread for a second time.')
									player.inventory.food[i] = deepcopy(il.ilist['food'][8])#turn a bread into rusk
								elif player.inventory.food[i].techID == il.ilist['food'][9].techID: #this is raw meat
									message.add('You grill raw meat.')
									player.inventory.food[i] = deepcopy(il.ilist['food'][10])#turn a fish into a grilled fish
								elif player.inventory.food[i].techID == il.ilist['food'][11].techID: #this is a cult. mushroom
									message.add('You grill a mushroom.')
									player.inventory.food[i] = deepcopy(il.ilist['food'][12])#turn a cult. mushroom into a grilled mushroom
								elif player.inventory.food[i].techID == il.ilist['food'][25].techID: #this is a jellyfish
									message.add('You grill a jellyfish.')
									player.inventory.food[i] = deepcopy(il.ilist['food'][26])#turn a jellyfish into a grilled jellyfish
								elif player.inventory.food[i].techID == il.ilist['food'][0].techID: #this are red berries
									message.add('You make some red jelly.')
									player.inventory.food[i] = deepcopy(il.ilist['food'][29])#turn red berries into red jelly
								elif player.inventory.food[i].techID == il.ilist['food'][27].techID: #this are blue berries
									message.add('You make some blue jelly.')
									player.inventory.food[i] = deepcopy(il.ilist['food'][30])#turn blue berries into blue jelly
								elif player.inventory.food[i].techID == il.ilist['food'][28].techID: #this are red berries
									message.add('You make some yellow jelly.')
									player.inventory.food[i] = deepcopy(il.ilist['food'][31])#turn yellow berries into yellow jelly
								
								####add more here
								
						run = False
						
					else:
							
						message.add('You have not enough wood!')
						run = False
						
				elif ui == 'x':
					
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'altar':
			 #this is a altar
			
			run = True
			
			while run:
				
				screen.render_request('['+key_name['e']+'] - pray', '['+key_name['b']+'] - identify ', '['+key_name['x']+'] - leave')
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					
					judgement = gods.judgement() # see if the player is supported by the gods
					
					if judgement == True:
						
						cursed_items = 0
						bodyparts = ('Hold(R)', 'Hold(L)', 'Head', 'Body', 'Legs', 'Feet', 'Hand', 'Neck')
						
						for i in bodyparts:#check if player wears some cursed equipment
							
							if player.inventory.wearing[i].cursed < 1 and i != player.inventory.nothing:
								cursed_items += 1
						
						if (player.lp*100)/player.attribute.max_lp < 20:#player has less then 20% of lp -> heal
							player.lp = player.attribute.max_lp
							message.add('The gods heal your wounds.')
							gods.mood -= 10
							run = False
							
						elif (player.attribute.hunger*100)/player.attribute.hunger_max < 20 or (player.attribute.thirst*100)/player.attribute.thirst_max < 20 or (player.attribute.tiredness*100)/player.attribute.tiredness_max < 20:
							#player is very hungry,thirsty or tired -> refresh
							player.attribute.hunger = player.attribute.hunger_max
							player.attribute.thirst = player.attribute.thirst_max
							player.attribute.tiredness = player.attribute.tiredness_max
							message.add('The gods rerfresh you.')
							gods.mood -= 10
							run = False
							
						elif cursed_items > 0:#player has some cursed items
							
							bodyparts = ('Hold(R)', 'Hold(L)', 'Head', 'Body', 'Legs', 'Feet', 'Hand', 'Neck')
							
							for j in bodyparts:
								
								if player.inventory.wearing[j].cursed < 1 and player.inventory.wearing[j] != player.inventory.nothing:
									player.inventory.wearing[j].cursed = 1
									player.inventory.wearing[j].set_name()
							
							message.add('The gods remove curses from your equipment.')
							gods.mood -= 10
							run = False
						
						else:
							message.add('The gods are pleased about you.')
							run = False
							
					else: 
						
						uncursed_items = 0
						bodyparts = ('Hold(R)', 'Hold(L)', 'Head', 'Body', 'Legs', 'Feet', 'Hand', 'Neck')
						
						for i in bodyparts:#check if player wears some cursed equipment
							
							if player.inventory.wearing[i].cursed > 0 and player.inventory.wearing[i] != player.inventory.nothing:
								uncursed_items += 1
						
						if uncursed_items > 0:
							
							for j in bodyparts:
								
								if player.inventory.wearing[j].cursed > 0 and player.inventory.wearing[j] != player.inventory.nothing:
									player.inventory.wearing[j].cursed = 0
									player.inventory.wearing[j].set_name()
							
							message.add('The gods are angry and curse your equipment.')
							run = False
						else:
							
							player.lp -= 5
							message.add('The gods are angry and hurt you')
							run = False
				
				
				elif ui == 'b':
					
					bodyparts = ('Hold(R)', 'Hold(L)', 'Head', 'Body', 'Legs', 'Feet', 'Hand', 'Neck')
					
					for i in bodyparts:
						
						if player.inventory.wearing[i] != player.inventory.nothing:
							player.inventory.wearing[i].identification()
							
					for j in range (0, len(player.inventory.equipment)):
						
						if player.inventory.equipment[j] != player.inventory.nothing:
							player.inventory.equipment[j].identification()
							
					message.add('Now you are aware of your equipments states.')
					run = False
					
				elif ui == 'x':
					
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'go_desert':
			pos = world.maplist[self.pos[2]]['desert_0_0'].find_first(tl.tlist['extra'][7])
			pos[1] += 1
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.pos[2] = 0#only to be sure
			player.on_map = 'desert_0_0'
			player.stand_check()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'return_desert':
			pos = world.maplist[self.pos[2]]['local_0_0'].find_first(tl.tlist['extra'][6])
			pos[1] -= 1
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.pos[2] = 0#only to be sure
			player.on_map = 'local_0_0'
			player.stand_check()
								
		elif world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:#interaction with a container eg.: a chest
			
			world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'shop' or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['shop'][0].techID:#this is shop floor
			
			if world.maplist[self.pos[2]][self.on_map].map_type == 'grot':
				list_items = ('Scroll of Return(1 Gem)','Enchanted Enhancement Powder(5 Gem)','Copper Pickaxe(3 Gem)','Copper Axe(3 Gem)', 'Grilled Fish(1 Gem)', 'Torch(1 Gem)')
				prices = (1,5,3,3,1,1)
				axe = item_wear('axe',11,0)
				pickaxe = item_wear('pickaxe',11,0)
				items = (il.ilist['misc'][33],il.ilist['misc'][42],pickaxe,axe,il.ilist['food'][5],il.ilist['misc'][44])
			elif world.maplist[self.pos[2]][self.on_map].map_type == 'elfish_fortress':
				list_items = ('Scroll of Return(1 Gem)','Mysterious Blue Crystal(10 Gem)','Steel Pickaxe(5 Gem)','Steel Axe(5 Gem)', 'Red Berries(1 Gem)', 'Torch(1 Gem)')
				prices = (1,10,5,5,1,1)
				axe = item_wear('axe',15,0)
				pickaxe = item_wear('pickaxe',15,0)
				items = (il.ilist['misc'][33],il.ilist['misc'][41],pickaxe,axe,il.ilist['food'][0],il.ilist['misc'][44])
			elif world.maplist[self.pos[2]][self.on_map].map_type == 'orcish_mines':
				list_items = ('Scroll of Return(1 Gem)','Bomb(7 Gem)','Titan Pickaxe(7 Gem)','Titan Axe(7 Gem)', 'Grilled Meat(1 Gem)', 'Torch(1 Gem)')
				prices = (1,7,7,7,1,1)
				axe = item_wear('axe',18,0)
				pickaxe = item_wear('pickaxe',18,0)
				items = (il.ilist['misc'][33],il.ilist['misc'][24],pickaxe,axe,il.ilist['food'][10],il.ilist['misc'][44])
			else:#only for fallback
				list_items = ('Scroll of Return(1 Gem)','Heavy Bag(5 Gem)','Wooden Pickaxe(1 Gem)','Wooden Axe(1 Gem)', 'Grilled Fish(1 Gem)', 'Torch(1 Gem)')
				prices = (1,5,1,1,1,1)
				axe = item_wear('axe',0,0)
				pickaxe = item_wear('pickaxe',0,0)
				items = (il.ilist['misc'][33],il.ilist['misc'][43],pickaxe,axe,il.ilist['food'][5],il.ilist['misc'][44])
			headline = 'You have ' + str(player.inventory.materials.gem) + ' gems. What do you want to buy?'
			choice = screen.get_choice(headline,list_items,True)
			if choice != 'Break':
				if prices[choice] <= player.inventory.materials.gem:
					world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choice]])
					test = world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].loot(0)
					world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = 0#del the container to be sure
					if test == True:
						player.inventory.materials.gem -= prices[choice]
						message.add('The shopkeeper thanks you for your purchacing.')
					else:
						message.add('Your bags are to full to buy this item.')
				else:
					message.add('You havn\'t enough gems to buy this item.')
			else:
				message.add('Never Mind.')
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'grassland_down':#this is a grassland dungeon stair down
			plus = world.maplist[self.pos[2]][self.on_map].monster_plus
			if plus < 5:
				world.dungeon_generator(plus+1,True)
			else:
				world.dungeon_generator(plus+1,False)
				
			if player.on_map != 'dungeon_0_0':
				player.last_z = player.pos[2]
				
			player.on_map = 'dungeon_0_0'
			player.pos[2] = 1
			
			pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][8])
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.stand_check()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'grassland_up':#this is a grassland dungeon stair up
			choose = screen.get_choice('Do you want to give up?',['No','Yes'],True)
			if choose == 1:
				player.on_map = player.last_map
				player.pos[2] = player.last_z
				
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][7])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.stand_check()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'tomb_down':#this is a grassland dungeon stair down
			plus = world.maplist[self.pos[2]][self.on_map].monster_plus
			if plus < 3:
				world.dungeon_generator(plus+1,stair_down=True,style='Tomb')
			else:
				world.dungeon_generator(plus+1,stair_down=False,style='Tomb')
			
			if player.on_map != 'dungeon_0_0':
				player.last_z = player.pos[2]
				
			player.on_map = 'dungeon_0_0'
			player.pos[2] = 1
			
			pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][19])
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.stand_check()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'tomb_up':#this is a grassland dungeon stair up
			choose = screen.get_choice('Do you want to give up?',['No','Yes'],True)
			if choose == 1:
				player.on_map = player.last_map
				player.pos[2] = player.last_z
				
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][18])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.stand_check()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'grot_down':#this is a grassland dungeon stair down
			plus = world.grot_generator(1)
				
			if player.on_map != 'dungeon_0_0':
				player.last_z = player.pos[2]
				
			player.on_map = 'dungeon_0_0'
			player.pos[2] = 1
			
			pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][15])
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.stand_check()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'grot_up':#this is a grassland dungeon stair up
			choose = screen.get_choice('Do you want to leave?',['No','Yes'],True)
			if choose == 1:
				player.on_map = player.last_map
				player.pos[2] = player.last_z
				
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][14])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.stand_check()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'mine_down':#this is a grassland dungeon stair down
			plus = world.mine_generator(1)
				
			if player.on_map != 'dungeon_0_0':
				player.last_z = player.pos[2]
				
			player.on_map = 'dungeon_0_0'
			player.pos[2] = 1
			
			pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][17])
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.stand_check()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'mine_up':#this is a grassland dungeon stair up
			choose = screen.get_choice('Do you want to leave?',['No','Yes'],True)
			if choose == 1:
				player.on_map = player.last_map
				player.pos[2] = player.last_z
				
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][16])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.stand_check()
			
		else:
			wait_10m = '['+key_name['e']+'] - Wait 10 minute'
			wait_30m = '['+key_name['b']+'] - Wait 30 minutes'
			wait_1h = '['+key_name['i']+'] - Wait 1 hour'
			screen.render_request(wait_10m,wait_30m,wait_1h)
			
			run = True
			while run:
				turns = 0
				
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					turns = 9
					run = False
				elif ui == 'b':
					run = False
					turns = 29
				elif ui == 'i':
					turns = 59
					run = False
				elif ui == 'x':
					return
				
				
				if turns > 0:
					old_lp = player.lp	
					while turns > 0:
						old_lp = player.lp
						hostile_count = 0
						
						for my in range(player.pos[1]-2,player.pos[1]+3):
							for mx in range(player.pos[0]-2,player.pos[0]+3):
								try:
									if world.maplist[self.pos[2]][self.on_map].npcs[my][mx] != 0:
										if world.maplist[self.pos[2]][self.on_map].npcs[my][mx].AI_style == 'hostile':
											hostile_count += 1
								except:
									None
								
						
						if (player.attribute.hunger*100)/player.attribute.hunger_max < 10:
							message.add('You feel to hungry to wait any longer.')
							return
						elif (player.attribute.thirst*100)/player.attribute.thirst_max < 10:
							message.add('You feel to thirsty to wait any longer.')
							return
						elif (player.attribute.tiredness*100)/player.attribute.tiredness_max < 10:
							message.add('You feel to tired to wait any longer.')
							return
						elif hostile_count == 1:
							message.add('You are interupted by a monster.')
							return
						elif hostile_count > 1:
							message.add('You are interupted by a group of monsters.')
							return
						
						time.tick()
						if player.lp < old_lp:
							message.add('Something hurts you!')
							return
						turns -= 1
					
			
			#message.add('There is nothing to interact with at this place.')
			
class player_class(mob):
	
	def __init__(self, name, on_map, attribute, inventory, pos =[10,10,0], build='Manual'):
		
		lname = save_path + os.sep + 'player.data'
		
		try:
			
			mob.__init__(self, name, on_map, attribute, pos)
			
			f = open(lname, 'rb')
			screen.render_load(7)
			temp = p.load(f)
			
			self.name = temp.name
			self.on_map = temp.on_map
			
			self.gender = temp.gender
			self.style = temp.style
			self.difficulty = temp.difficulty
			
			#attribute
			self.attribute.p_strength = temp.attribute.p_strength
			self.attribute.p_defense = temp.attribute.p_defense
			self.attribute.m_strength = temp.attribute.m_strength
			self.attribute.m_defense = temp.attribute.m_defense
			self.attribute.luck = temp.attribute.luck
			self.attribute.max_lp = temp.attribute.max_lp
			self.attribute.max_mp = temp.attribute.max_mp
			self.lp = temp.lp
			self.mp = temp.mp
			self.attribute.hunger_max = temp.attribute.hunger_max
			self.attribute.hunger = temp.attribute.hunger
			self.attribute.thirst_max = temp.attribute.thirst_max
			self.attribute.thirst = temp.attribute.thirst
			self.attribute.tiredness_max = temp.attribute.tiredness_max
			self.attribute.tiredness = temp.attribute.tiredness
			self.attribute.pickaxe_power = temp.attribute.pickaxe_power
			
			self.inventory = temp.inventory
			self.pos = temp.pos
			
			self.buffs = temp.buffs
			self.xp = temp.xp
			self.lvl = temp.lvl
			
			self.cur_map = temp.cur_map
			self.last_map = temp.last_map
			self.cur_z = temp.cur_z
			self.last_z = temp.last_z
			
		except:
			if build == 'Manual':
				accept = False
				while accept == False:
				
					num = 0
					gender_list = ('FEMALE','MALE') 
					run = True
					
					if low_res == False:
						marker_y = 115
					else:
						marker_y = 46
					
					while run:
					
						if low_res == False:
							s = pygame.Surface((640,360))
						else:
							s = pygame.Surface((320,240))
				
						bg = pygame.Surface((480,360))
						bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
						if low_res == True:
							bg = pygame.transform.scale(bg,(320,240))

						s.blit(bg,(0,0))
				
						text_image = screen.font.render('Choose gender:',1,(255,255,255))
						s.blit(text_image,(5,2))#menue title
				
						s.blit(gra_files.gdic['display'][4],(0,marker_y+num*25))#blit marker
				
						for i in range (0,2): 
							string = gender_list[i]
							text_image = screen.font.render(string,1,(0,0,0))
							s.blit(text_image,(21,(marker_y+5)+i*25))#blit item names
						
						text = '['+key_name['e']+'] - Choose'
						text_image = screen.font.render(text,1,(255,255,255))
						if low_res == False:
							s.blit(text_image,(5,335))
						else:
							s.blit(text_image,(2,225))
					
						if game_options.mousepad == 1 and low_res == False:
							s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
						else:
							s_help = pygame.Surface((160,360))
							s_help.fill((48,48,48))
							s.blit(s_help,(480,0))
					
						if game_options.mousepad == 0 and low_res == False:
							s_help = pygame.Surface((640,360))
							s_help.fill((48,48,48))
							s_help.blit(s,(80,0))
							s = s_help
						
						if low_res == False:
							s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
						
						screen.screen.blit(s,(0,0))
					
						pygame.display.flip()
					
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
						if ui == 's':
							num += 1
							if num > 1:
								num = 0
						
						if ui == 'w':
							num -= 1
							if num < 0:
								num = 1
						
						if ui == 'e':
							self.gender = gender_list[num]
							run = False
					
					run2 = True
					num2 = 0
				
					while run2:
						
						if low_res == False:
							s = pygame.Surface((640,360))
						else:
							s = pygame.Surface((320,240))
				
						bg = pygame.Surface((480,360))
						bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
						if low_res == True:
							bg = pygame.transform.scale(bg,(320,240))

						s.blit(bg,(0,0))
						
						text_image = screen.font.render('Choose style:',1,(255,255,255))
						s.blit(text_image,(5,2))#menue title
				
						s.blit(gra_files.gdic['display'][4],(0,marker_y+num2*32))#blit marker
				
						for i in range (1,5): 
							skinstring = 'SKIN_' + self.gender + '_' + str(i)
							hairstring = 'HAIR_' + self.gender + '_' +  str(i)
							s.blit(gra_files.gdic['char'][skinstring],(26,marker_y+(i-1)*32))
							s.blit(gra_files.gdic['char'][hairstring],(26,marker_y+(i-1)*32))
						
						text = '['+key_name['e']+'] Choose'
						text_image = screen.font.render(text,1,(255,255,255))
						if low_res == False:
							s.blit(text_image,(5,335))
						else:
							s.blit(text_image,(2,225))
					
						if game_options.mousepad == 1 and low_res == False:
							s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
						else:
							s_help = pygame.Surface((160,360))
							s_help.fill((48,48,48))
							s.blit(s_help,(480,0))
					
						if game_options.mousepad == 0 and low_res == False:
							s_help = pygame.Surface((640,360))
							s_help.fill((48,48,48))
							s_help.blit(s,(80,0))
							s = s_help
						
						if low_res == False:
							s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
						
						screen.screen.blit(s,(0,0))
					
						pygame.display.flip()
				
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
						if ui == 's':
							num2 += 1
							if num2 > 3:
								num2 = 0
						
						if ui == 'w':
							num2 -= 1
							if num2 < 0:
								num2 = 3
						
						if ui == 'e':
							self.style = num2
							run2 = False
					
			
					num3 = 0
					dificulty_list = ('EASY','NORMAL','HARD','ROGUELIKE','SANDBOX')
					description_list = ('Lose resources on death.','Lose inventory on death.','Lose inventory and level on death.','LOSE EVERYTHING', 'MONSTERS IGNORE YOU') 
					run3 = True
			
					while run3:
					
						if low_res == False:
							s = pygame.Surface((640,360))
						else:
							s = pygame.Surface((320,240))
				
						bg = pygame.Surface((480,360))
						bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
						if low_res == True:
							bg = pygame.transform.scale(bg,(320,240))

						s.blit(bg,(0,0))
						
						text_image = screen.font.render('Choose Game Mode:',1,(255,255,255))
						s.blit(text_image,(5,2))#menue title
				
						s.blit(gra_files.gdic['display'][4],(0,marker_y+num3*25))#blit marker
				
						for i in range (0,5): 
							string = dificulty_list[i]
							text_image = screen.font.render(string,1,(0,0,0))
							s.blit(text_image,(21,(marker_y+5)+i*25))#blit item names
					
							text_image = screen.font.render(description_list[num3],1,(255,255,255))
							if low_res == False:
								s.blit(text_image,(5,335))
							else:
								s.blit(text_image,(2,225))
						
						if game_options.mousepad == 1 and low_res == False:
							s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
						else:
							s_help = pygame.Surface((160,360))
							s_help.fill((48,48,48))
							s.blit(s_help,(480,0))
					
						if game_options.mousepad == 0 and low_res == False:
							s_help = pygame.Surface((640,360))
							s_help.fill((48,48,48))
							s_help.blit(s,(80,0))
							s = s_help
						
						if low_res == False:
							s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
						
						screen.screen.blit(s,(0,0))
					
						pygame.display.flip()
					
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
						if ui == 's':
							num3 += 1
							if num3 > 4:
								num3 = 0
						
						if ui == 'w':
							num3 -= 1
							if num3 < 0:
								num3 = 4
						
						if ui == 'e':
							self.difficulty = num3
							run3 = False
					
					name = screen.string_input('Whats your name?', 15)
					
					if name == '':
						name = 'Nameless' 
				
					num4 = 0
					choose_list = ('Yes','No') 
					run4 = True
					
					if low_res == False:
						char_x = 160
					else:
						char_x = 60
											
					while run4:
					
						if low_res == False:
							s = pygame.Surface((640,360))
						else:
							s = pygame.Surface((320,240))
				
						bg = pygame.Surface((480,360))
						bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
						if low_res == True:
							bg = pygame.transform.scale(bg,(320,240))

						s.blit(bg,(0,0))
						
						text_image = screen.font.render('Is everything alright?',1,(255,255,255))
						s.blit(text_image,(5,2))#menue title
					
						skinstring = 'SKIN_' + self.gender + '_' + str(self.style +1)
						s.blit(gra_files.gdic['char'][skinstring],(char_x,80))
						
						hairstring = 'HAIR_' + self.gender + '_' + str(self.style +1)
						s.blit(gra_files.gdic['char'][hairstring],(char_x,80))
					
						n_string = 'NAME: ' + name
						name_image = screen.font.render(n_string,1,(0,0,0))
						s.blit(name_image,(char_x,120))
					
						d_list = ('Easy', 'Normal', 'Hard', 'Rougelike', 'Sandbox')
					
						d_string = 'Difficulty: ' + d_list[self.difficulty]
						name_image = screen.font.render(d_string,1,(0,0,0))
						s.blit(name_image,(char_x,140))
					
						s.blit(gra_files.gdic['display'][4],(char_x-5,160+num4*25))#blit marker
				
						for i in range (0,2): 
							string = choose_list[i]
							text_image = screen.font.render(string,1,(0,0,0))
							s.blit(text_image,(char_x+16,165+i*25))#blit item names
						
						text = '['+key_name['e']+'] Choose'
						text_image = screen.font.render(text,1,(255,255,255))
						if low_res == False:
							s.blit(text_image,(5,335))
						else:
							s.blit(text_image,(2,225))
					
						if game_options.mousepad == 1 and low_res ==  False:
							s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
						else:
							s_help = pygame.Surface((160,360))
							s_help.fill((48,48,48))
							s.blit(s_help,(480,0))
					
						if game_options.mousepad == 0 and low_res == False:
							s_help = pygame.Surface((640,360))
							s_help.fill((48,48,48))
							s_help.blit(s,(80,0))
							s = s_help
						
						if low_res == False:
							s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
						
						screen.screen.blit(s,(0,0))
					
						pygame.display.flip()
					
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
						if ui == 's':
							num4 += 1
							if num4 > 1:
								num4 = 0
						
						if ui == 'w':
							num4 -= 1
							if num4 < 0:
								num4 = 1
						
						if ui == 'e':
						
							if num4 == 0:
								accept = True
							
							run4 = False
						
				if self.difficulty == 4:
				
					for i in range (0,len(world.maplist)-1):
					
						for y in range(0,max_map_size):
							for x in range(0,max_map_size):
							
								if world.maplist[i]['local_0_0'].npcs[y][x] != 0:
									world.maplist[i]['local_0_0'].npcs[y][x].AI_style = 'ignore'
								try:	
									if world.maplist[i]['desert_0_0'].npcs[y][x] != 0:
										world.maplist[i]['desert_0_0'].npcs[y][x].AI_style = 'ignore'
								except:
									None
					
			###############
			mob.__init__(self, name, on_map, attribute, pos)
		
			self.inventory = inventory
			
			self.xp = 0
			self.lvl = 0
			
			self.buffs = buffs()
			
			try:
				self.pos[0] = world.startx
				self.pos[1] = world.starty
			except:
				self.pos[0] = 0
				self.pos[1] = 0
			
			screen.render_load(5)
		
	def user_input(self,immobilized=False):
		
		ui = getch(screen.displayx,screen.displayy,0,game_options.turnmode,mouse=game_options.mousepad)
		
		if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
		
		if immobilized == True:
			if ui != 'x':
				ui = 'none'
		
		if ui == 'w':
			if screen.fire_mode == 0:
				self.move(0,-1)
				time.tick()
			else:
				self.player_fire((0,-1))
				screen.fire_mode = 0
				time.tick()
			
		if ui == 's':
			if screen.fire_mode == 0:
				self.move(0,1)
				time.tick()
			else:
				self.player_fire((0,1))
				screen.fire_mode = 0
				time.tick()
			
		if ui == 'a':
			if screen.fire_mode == 0:
				self.move(-1,0)
				time.tick()
			else:
				self.player_fire((-1,0))
				screen.fire_mode = 0
				time.tick()
			
		if ui == 'd':
			if screen.fire_mode == 0:
				self.move(1,0)
				time.tick()
			else:
				self.player_fire((1,0))
				screen.fire_mode = 0
				time.tick()
			
		if ui == 'e':
			if screen.fire_mode == 0:
				self.enter()
				time.tick()
		
		if ui == 'i':
			sfx.play('loot')
			self.inventory.inv_user_interaction()
			time.tick()
			
		if ui == 'b':
			if screen.fire_mode == 0:
				if world.maplist[self.pos[2]][self.on_map].build_type != 'None':
					self.built()
					time.tick()
				else:
					message.add('You can\'t build here!')
		
		if ui == 'f':
			if screen.fire_mode == 0:
				if player.inventory.wearing['Hold(L)'] != player.inventory.nothing:
					screen.fire_mode = 1
					message.add('You channelise your magic powers.')
				else:
					message.add('You need a magic weapon.')
			
		if ui == 'x':
			if screen.fire_mode == 0:
				screen.render_brake()
			else:
				screen.fire_mode = 0
			
		if ui == 'none':
			time.tick()
			player.stand_check()
			
	def lvl_up(self):
		
		sfx.play('lvl_up')
		
		self.lvl += 1
		self.xp -= 100
		
		if self.inventory.materials.wood_max < 200:
			self.inventory.materials.wood_max += 10
			if self.inventory.materials.wood_max > 200:
				self.inventory.materials.wood_max = 200
		
		if self.inventory.materials.stone_max < 200:
			self.inventory.materials.stone_max += 10
			if self.inventory.materials.stone_max > 200:
				self.inventory.materials.stone_max = 200
		
		if self.inventory.materials.ore_max < 30:
			self.inventory.materials.ore_max += 1
			if self.inventory.materials.ore_max > 30:
				self.inventory.materials.ore_max = 30
		
		if self.inventory.materials.herb_max < 30:
			self.inventory.materials.herb_max += 1
			if self.inventory.materials.herb_max > 30:
				self.inventory.materials.herb_max = 30
				
		if self.inventory.materials.gem_max < 30:
			self.inventory.materials.gem_max += 1
			if self.inventory.materials.gem_max > 30:
				self.inventory.materials.gem_max = 30		
		
		choices = []
		
		st_string = 'Strength(' + str(self.attribute.p_strength) + ' -> ' + str(self.attribute.p_strength+3) +')'
		choices.append(st_string)
		
		sk_string = 'Skill(' + str(self.attribute.p_defense) + ' -> ' + str(self.attribute.p_defense+3) +')'
		choices.append(sk_string)
		
		po_string = 'Power(' + str(self.attribute.m_strength) + ' -> ' + str(self.attribute.m_strength+3) +')'
		choices.append(po_string)
		
		wi_string = 'Will(' + str(self.attribute.m_defense) + ' -> ' + str(self.attribute.m_defense+3) +')'
		choices.append(wi_string)
		
		if self.attribute.max_lp < 20:
			he_string = 'Health(' + str(self.attribute.max_lp) + ' -> ' + str(self.attribute.max_lp+1) +')'
			choices.append(he_string)
		
		c = screen.get_choice('~*Level up! Please choose an attribute.*~',choices,False)
		
		if c == 0:
			self.attribute.p_strength += 3
		elif c == 1:
			self.attribute.p_defense += 3
		elif c == 2:
			self.attribute.m_strength += 3
		elif c == 3:
			self.attribute.m_defense += 3
		else:
			self.attribute.max_lp += 1
		
	def built(self):
		
		style = 'wall'
		
		xymin = 0
		xymax = 5
		
		xmin = xymin
		xmax = xymin
		ymin = xymin
		ymax = xymin
		
		run = True
		
		while run:
			
			res_need = screen.render_built(xmin,xmax,ymin,ymax,style)
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'w':
				
				if style != 'Door' and style != 'Stair up' and style != 'Stair down':
					if player.pos[1]-ymin > 0:
						ymin += 1
				
					if ymin >= xymax:
						ymin = xymin
				
				else:
					if ymin >= -3 and player.pos[1]+ymin > 0:
						ymin -= 1
					
			if ui == 's':
				
				if style != 'Door' and style != 'Stair up' and style != 'Stair down':
					if player.pos[1]+ymax < max_map_size-1:
						ymax += 1
				
					if ymax >= xymax:
						ymax = xymin
					
				else:
					if ymin <= 3 and player.pos[1]+ymin < max_map_size-1:
						ymin += 1
					
			if ui == 'a':
				if style != 'Door' and style != 'Stair up' and style != 'Stair down':
					if player.pos[0]-xmin > 0:
						xmin += 1
				
					if xmin >= xymax:
						xmin = xymin
						
				else:
					if xmin >= -3 and player.pos[0]+xmin > 0:
						xmin -= 1
					
			if ui == 'd':
				if style != 'Door' and style != 'Stair up' and style != 'Stair down':
					if player.pos[0]+xmax < max_map_size-1:
						xmax += 1
				
					if xmax >= xymax:
						xmax = xymin
				
				else:
					if xmin <= 3 and player.pos[0]+xmin < max_map_size-1:
						xmin += 1
					
			
			if ui == 'b':
				
				xmax = xymin
				xmin = xymin
				ymax = xymin
				ymin = xymin
				
				if style == 'wall':
					style = 'floor'
					
				elif style == 'floor':
					style = 'Door'
					
				elif style == 'Door':
					if world.maplist[self.pos[2]][self.on_map].build_type != 'Part':
						style = 'Stair up'
					else:
						style = 'Agriculture'
					
				elif style == 'Stair up':
					style = 'Stair down'
				
				elif style == 'Stair down':
					style = 'Agriculture'
					
				elif style == 'Agriculture':
					style = 'remove'	
					
				elif style == 'remove':
					style = 'wall'
			
			if ui == 'e':
				if style == 'wall':
					if res_need[0] <= player.inventory.materials.wood and res_need[1] <= player.inventory.materials.stone:
					
						player.inventory.materials.wood -= res_need[0]
						player.inventory.materials.stone -= res_need[1]
					
						for y in range (-ymin,ymax+1):
							for x in range (-xmin,xmax+1):
				
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] == 0:
									built_here = True
								elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
									built_here = True
								else: 
									built_here = False
									
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
									built_here = False
							
								if built_here == True:
									
									world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+y][player.pos[0]+x] = 0 #first of all erase all items that are at this pos
									
									if x == xmax or x == -xmin or y == ymax or y == -ymin:
										if x == xmax or x == -xmin:
												world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist[player.inventory.blueprint.place_cat][player.inventory.blueprint.place_num+1] #set a wall here
					
										if y == ymax or y == -ymin:
												world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist[player.inventory.blueprint.place_cat][player.inventory.blueprint.place_num+1] #set a wall here
									else:
										None
					else: 
						message.add('Not enough Resources.')
				
				elif style == 'floor':
					if res_need[0] <= player.inventory.materials.wood and res_need[1] <= player.inventory.materials.stone:
					
						player.inventory.materials.wood -= res_need[0]
						player.inventory.materials.stone -= res_need[1]
					
						for y in range (-ymin,ymax+1):
							for x in range (-xmin,xmax+1):
				
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] == 0:
									built_here = True
								elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
									built_here = True
								else: 
									built_here = False
								
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
									built_here = False
								
								if built_here == True:
									
									world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+y][player.pos[0]+x] = 0 #first of all erase all items that are at this pos
									if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].replace != None:
										world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].replace = tl.tlist[player.inventory.blueprint.place_cat][player.inventory.blueprint.place_num]
									else:
										world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist[player.inventory.blueprint.place_cat][player.inventory.blueprint.place_num] #set floor here
					
					else: 
						message.add('Not enough Resources.')
				
				elif style == 'Door':
					
					if res_need[0] <= player.inventory.materials.wood and res_need[1] <= player.inventory.materials.stone:
					
						player.inventory.materials.wood -= res_need[0]
						player.inventory.materials.stone -= res_need[1]
						
						if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] == 0:
							built_here = True
						elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].civilisation == True:
							built_here = True
						else: 
							built_here = False
								
						if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == False:
							built_here = False
								
						if built_here == True:
								
							world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+ymin][player.pos[0]+xmin] = 0 #first of all erase all items that are at this pos
									
							world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = deepcopy(tl.tlist['building'][3]) #set door here
				
				elif style == 'Stair up':
					
					if res_need[0] <= player.inventory.materials.wood and res_need[1] <= player.inventory.materials.stone:
						if player.pos[2] > 0:
					
							if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].replace == None and world.maplist[player.pos[2]-1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0+xmin]].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False:
								build_here = 0
							else: 
								build_here = 1
							
							if build_here == 0:
								world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+ymin][player.pos[0]+xmin] = 0 #first of all erase all items that are at this pos
								world.maplist[player.pos[2]-1][player.on_map].containers[player.pos[1]+ymin][player.pos[0]+xmin] = 0
								player.inventory.materials.wood -= res_need[0]
								player.inventory.materials.stone -= res_need[1]
								world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = tl.tlist['functional'][2]
								world.maplist[player.pos[2]-1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = tl.tlist['functional'][1]
							else:
								message.add('Not here.')
					else:
						message.add('Not enough Resources.')
			
				elif style == 'Stair down':
					
					if res_need[0] <= player.inventory.materials.wood and res_need[1] <= player.inventory.materials.stone:
						if player.pos[2] < 15:
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].replace == None and world.maplist[player.pos[2]+1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].damage == False:
								build_here = 0
							else: 
								build_here = 1
							
							if build_here == 0:
								world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+ymin][player.pos[0]+xmin] = 0 #first of all erase all items that are at this pos
								world.maplist[player.pos[2]+1][player.on_map].containers[player.pos[1]+xmin][player.pos[0]+ymin] = 0
								player.inventory.materials.wood -= res_need[0]
								player.inventory.materials.stone -= res_need[1]
								world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = tl.tlist['functional'][1]
								world.maplist[player.pos[2]+1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = tl.tlist['functional'][2]
							else:
								message.add('Not here.')
					else:
						message.add('Not enough Resources')
				
				elif style == 'Agriculture':
					if res_need[0] <= player.inventory.materials.seeds:
					
						player.inventory.materials.seeds -= res_need[0]
					
						for y in range (-ymin,ymax+1):
							for x in range (-xmin,xmax+1):
				
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] == 0:
									built_here = True
								elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
									built_here = True
								else: 
									built_here = False
								
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
									built_here = False
								
								if built_here == True:
									
									world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+y][player.pos[0]+x] = 0 #first of all erase all items that are at this pos
									
									world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist['building'][4] #set aggriculture here
					
					else: 
						message.add('Not enough Resources.')
					
				elif style == 'remove':
					
					for y in range (-ymin,ymax+1):
							for x in range (-xmin,xmax+1):
					
								if player.pos[2] == 0:
									if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == True:
										world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+y][player.pos[0]+x] = 0 #first of all erase all items that are at this pos
										world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist['local'][0] #set gras here
								elif player.pos[2] != 0 and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == True:
									if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
										world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+y][player.pos[0]+x] = 0 #first of all erase all items that are at this pos
										world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist['global_caves'][0] #set cave ground here	
				
				run = False
			
					
			if ui == 'x':
				
				run = False
		
	def monster_attacks(self,x,y):
		#This function is called when a monster attacks the player. The x and the y variable are to define the monsters pos 
		
		random_attack = None
		
		if world.maplist[self.pos[2]][self.on_map].npcs[y][x].behavior == 'attack_random':
			coin_random = random.randint(0,1)
			if coin_random == 0:
				random_attack = 'melee'
			else:
				random_attack = 'magic'
		
		if world.maplist[self.pos[2]][self.on_map].npcs[y][x].behavior == 'attack_melee' or random_attack == 'melee':
			
			bodypart = world.maplist[self.pos[2]][self.on_map].npcs[y][x].attack_were[random.randint(0,len(world.maplist[self.pos[2]][self.on_map].npcs[y][x].attack_were)-1)]
			
			monster_strength  = 0
			for i in range(0,world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.p_strength):
				 monster_strength += random.randint(1,6)
				 
			player_defense = 0
			for j in range(0,self.attribute.p_defense + self.inventory.wearing[bodypart].attribute.p_defense):
				player_defense += random.randint(1,6)
			
			if monster_strength >= player_defense:
				attack_success = True
			else:
				attack_success = False
				
			if attack_success == False:#give the monster a chance to have luck and hit the player
				chance = random.randint(0,25)
				if chance < world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.luck:
					attack_success = True
					
			if world.maplist[self.pos[2]][self.on_map].npcs[y][x].move_border >= 9:
				attack_success = True
					
			if attack_success == True:
				
				chance = random.randint(0,25)
				
				if chance < world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.luck:#monster hits critical
					sfx.play('hit')
					message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + ' hits your ' + bodypart.lower() + ' critical!'
					screen.write_hit_matrix(player.pos[0],player.pos[1],5)
					message.add(message_string)
					player.lp -= 4
					if self.inventory.wearing[bodypart] != self.inventory.nothing:
						self.inventory.wearing[bodypart].take_damage()#your amor at this bodypart take twice damage
						self.inventory.wearing[bodypart].take_damage()
						if self.inventory.wearing[bodypart].state > 0:
							self.inventory.wearing[bodypart].set_name()
						else:
							self.inventory.wearing[bodypart] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing[bodypart].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
				else:
					sfx.play('hit')
					message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + ' hits your ' + bodypart.lower() + '!'
					message.add(message_string)
					screen.write_hit_matrix(player.pos[0],player.pos[1],4)
					player.lp -= 2
					if self.inventory.wearing[bodypart] != self.inventory.nothing:
						self.inventory.wearing[bodypart].take_damage()
						if self.inventory.wearing[bodypart].state > 0:
							self.inventory.wearing[bodypart].set_name()
						else:
							self.inventory.wearing[bodypart] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing[bodypart].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
						
				if world.maplist[self.pos[2]][self.on_map].npcs[y][x].possible_effect != None:
					
					chance = random.randint(0,99)
					
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].effect_probability > chance:
						player.buffs.set_buff(world.maplist[self.pos[2]][self.on_map].npcs[y][x].possible_effect,world.maplist[self.pos[2]][self.on_map].npcs[y][x].effect_duration)
						message.add(world.maplist[self.pos[2]][self.on_map].npcs[y][x].message)
				
			else:
				sfx.play('miss')
				message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + ' miss you!'
				message.add(message_string)
				screen.write_hit_matrix(player.pos[0],player.pos[1],3)
		
		elif world.maplist[self.pos[2]][self.on_map].npcs[y][x].behavior == 'attack_magic' or random_attack == 'magic':
			
			monster_strength = 0
			for i in range(world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.m_strength):
				monster_strength += random.randint(1,6)
				
			player_defense = 0
			for j in range(0,player.attribute.p_defense + player.inventory.wearing['Neck'].attribute.m_defense + self.inventory.wearing['Hand'].attribute.m_defense):
				player_defense += random.randint(1,6)
			
			if monster_strength >= player_defense:
				attack_success = True
			else:
				attack_success = False
				
			if attack_success == False:#give the monster a chance to have luck and hit the player
				chance = random.randint(0,25)
				if chance < world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.luck:
					attack_success = True
					
			if world.maplist[self.pos[2]][self.on_map].npcs[y][x].move_border >= 9:
				attack_success = True
					
			if attack_success == True:
				
				chance = random.randint(0,25)
				
				if chance < world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.luck:#monster hits critical
					sfx.play('hit')
					message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '\'s magic attack hits you critical!'
					message.add(message_string)
					screen.write_hit_matrix(player.pos[0],player.pos[1],5)
					player.lp -= 4
					if self.inventory.wearing['Neck'] != self.inventory.nothing:
						self.inventory.wearing['Neck'].take_damage()#your amor at this bodypart take twice damage
						self.inventory.wearing['Neck'].take_damage()
						if self.inventory.wearing['Neck'].state > 0:
							self.inventory.wearing['Neck'].set_name()
						else:
							self.inventory.wearing['Neck'] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing['Neck'].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
						
					if self.inventory.wearing['Hand'] != self.inventory.nothing:
						self.inventory.wearing['Hand'].take_damage()#your amor at this bodypart take twice damage
						self.inventory.wearing['Hand'].take_damage()
						if self.inventory.wearing['Hand'].state > 0:
							self.inventory.wearing['Hand'].set_name()
						else:
							self.inventory.wearing['Hand'] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing['Hand'].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
				else:
					sfx.play('hit')
					message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '\'s magic attack hits you!'
					message.add(message_string)
					screen.write_hit_matrix(player.pos[0],player.pos[1],4)
					player.lp -= 2
					
					if self.inventory.wearing['Neck'] != self.inventory.nothing:
						self.inventory.wearing['Neck'].take_damage()
						if self.inventory.wearing['Neck'].state > 0:
							self.inventory.wearing['Neck'].set_name()
						else:
							self.inventory.wearing['Neck'] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing['Neck'].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
						
					if self.inventory.wearing['Hand'] != self.inventory.nothing:
						self.inventory.wearing['Hand'].take_damage()
						if self.inventory.wearing['Hand'].state > 0:
							self.inventory.wearing['Hand'].set_name()
						else:
							self.inventory.wearing['Hand'] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing['Hand'].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
				
				if world.maplist[self.pos[2]][self.on_map].npcs[y][x].possible_effect != None:
					
					chance = random.randint(0,99)
					
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].effect_probability > chance:
						player.buffs.set_buff(world.maplist[self.pos[2]][self.on_map].npcs[y][x].possible_effect,world.maplist[self.pos[2]][self.on_map].npcs[y][x].effect_duration)
						message.add(world.maplist[self.pos[2]][self.on_map].npcs[y][x].message)
					
			else:
				sfx.play('miss')
				message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '\'s magic attack miss you!'
				message.add(message_string)
				screen.write_hit_matrix(player.pos[0],player.pos[1],3)
		
		if self.lp <= 0:
			screen.render_dead()
	
	def attack_monster(self,x,y,style='melee'):
		#This function is called when the player try to move at the same position like a monster. The x and the y variable definates the monsters pos. 
		
		if world.maplist[self.pos[2]][self.on_map].npcs[y][x].behavior == 'talk':
			message.add(world.maplist[self.pos[2]][self.on_map].npcs[y][x].message)
			return 'Done'
		
		if style == 'magic':
			
			player_strength = 0
			for i in range(0,self.attribute.m_strength + self.inventory.wearing['Hold(L)'].attribute.m_strength + self.lvl):
				player_strength += random.randint(1,6)
				
			monster_defense = 0
			for j in range(0,world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.m_defense):
				monster_defense += random.randint(1,6)
			if world.maplist[self.pos[2]][self.on_map].npcs[y][x].move_border > 9:
				monster_defense = 0
			
			player_luck = self.attribute.luck + self.inventory.wearing['Hand'].attribute.luck +self.inventory.wearing['Neck'].attribute.luck
			
			if player_strength >= monster_defense:
				attack_success = True
			else:
				attack_success = False
				
			if attack_success == False:#let the player have luck and hit the monster
				chance = random.randint(0,25)
				if chance < self.attribute.luck:
					attack_success = True
					
			if attack_success == True:
				
				chance = random.randint(0,25)
				
				if chance < player_luck:#player hits critical
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'vase' and world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'monster vase':
						sfx.play('hit')
					else:
						sfx.play('shatter')
					message_string = 'Your magic attack hits the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + ' critical!'
					message.add(message_string)
					screen.write_hit_matrix(x,y,5)
					world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp -= 2
					 
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp <= 0:
						
						xp = world.maplist[self.pos[2]][self.on_map].npcs[y][x].lvl - self.lvl + 1
						if xp < 0:
							xp = 0
						self.xp += xp
						
						if self.xp >= 100:
							self.lvl_up()
						
						test = False
						while test == False:
							test = world.maplist[self.pos[2]][self.on_map].monster_die(x,y)	
						
					if self.inventory.wearing['Hold(L)'] != self.inventory.nothing:
						self.inventory.wearing['Hold(L)'].take_damage()
						if self.inventory.wearing['Hold(L)'].state > 0:
							self.inventory.wearing['Hold(L)'].set_name()
						else:
							self.inventory.wearing['Hold(L)'] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing['Hold(L)'].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
					 
				else:
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'vase' and world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'monster vase':
						sfx.play('hit')
					else:
						sfx.play('shatter')
					message_string = 'Your magic attack hits the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '!'
					message.add(message_string)
					screen.write_hit_matrix(x,y,4)
					world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp -= 1
					
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp <= 0:
						
						xp = world.maplist[self.pos[2]][self.on_map].npcs[y][x].lvl - self.lvl +1
						if xp < 0:
							xp = 0
						self.xp += xp
						
						if self.xp >= 100:
							self.lvl_up()
						
						test = False
						while test == False:
							test = world.maplist[self.pos[2]][self.on_map].monster_die(x,y)
					
					if self.inventory.wearing['Hold(L)'] != self.inventory.nothing:
						self.inventory.wearing['Hold(L)'].take_damage()
						if self.inventory.wearing['Hold(L)'].state > 0:
							self.inventory.wearing['Hold(L)'].set_name()
						else:
							self.inventory.wearing['Hold(L)'] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing['Hold(L)'].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
			else:
				sfx.play('miss')
				message_string = 'You miss the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '.'
				message.add(message_string)
				screen.write_hit_matrix(x,y,3)
		else:
			
			player_strength = 0
			for i in range(0,player.attribute.p_strength + player.inventory.wearing['Hold(R)'].attribute.p_strength):
				player_strength += random.randint(1,6)
				
			monster_defense = 0
			for i in range(0,world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.p_defense):
				monster_defense += random.randint(1,6)
			if world.maplist[self.pos[2]][self.on_map].npcs[y][x].move_border > 9:
				monster_defense = 0
			
			player_luck = self.attribute.luck + self.inventory.wearing['Hand'].attribute.luck +self.inventory.wearing['Neck'].attribute.luck
				
			if player_strength >= monster_defense:
				attack_success = True
			else:
				attack_success = False
				
			if attack_success == False:#let the player have luck and hit the monster
				chance = random.randint(0,25)
				if chance < player_luck:
					attack_success = True
			
			if attack_success == True:
				
				chance = random.randint(0,25)
				
				if chance < player_luck:#player hits critical
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'vase' and world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'monster vase':
						sfx.play('hit')
					else:
						sfx.play('shatter')
					message_string = 'You hit the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + ' critical!'
					message.add(message_string)
					screen.write_hit_matrix(x,y,5)
					world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp -= 2
					 
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp <= 0:
						
						xp = world.maplist[self.pos[2]][self.on_map].npcs[y][x].lvl - self.lvl +1
						
						if xp < 0:
							xp = 0
						self.xp += xp
						
						if self.xp >= 100:
							self.lvl_up()
						
						test = False
						while test == False:
							test = world.maplist[self.pos[2]][self.on_map].monster_die(x,y)	
					 
					if self.inventory.wearing['Hold(R)'] != self.inventory.nothing:
						self.inventory.wearing['Hold(R)'].take_damage()
						if self.inventory.wearing['Hold(R)'].state > 0:
							self.inventory.wearing['Hold(R)'].set_name()
						else:
							self.inventory.wearing['Hold(R)'] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing['Hold(R)'].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
					 
				else:
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'vase' and world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'monster vase':
						sfx.play('hit')
					else:
						sfx.play('shatter')
					message_string = 'You hit the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '!'
					message.add(message_string)
					screen.write_hit_matrix(x,y,4)
					world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp -= 1
					
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp <= 0:
						
						xp = world.maplist[self.pos[2]][self.on_map].npcs[y][x].lvl - self.lvl + 1
						
						if xp < 0:
							xp = 0
						self.xp += xp
						
						if self.xp >= 100:
							self.lvl_up()
						
						test = False
						while test == False:
							test = world.maplist[self.pos[2]][self.on_map].monster_die(x,y)	
					
					if self.inventory.wearing['Hold(R)'] != self.inventory.nothing:
						self.inventory.wearing['Hold(R)'].take_damage()
						if self.inventory.wearing['Hold(R)'].state > 0:
							self.inventory.wearing['Hold(R)'].set_name()
						else:
							self.inventory.wearing['Hold(R)'] = self.inventory.nothing
							mes = 'Your '+self.inventory.wearing['Hold(R)'].classe+' breaks!'
							message.add(mes)
							sfx.play('item_break')
			
			else:
				sfx.play('miss')
				message_string = 'You miss the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '.'
				message.add(message_string)
				screen.write_hit_matrix(x,y,3)
	
	def player_fire(self,direction):
		
		sfx.play('fire')
		#direction must be a tulpel like (0,1) [style: (x,y)]
		x=player.pos[0]
		y=player.pos[1]
		c = 1
		run = True
		
		while run:
			
			xx = player.pos[0] + (direction[0]*c)
			yy = player.pos[1] + (direction[1]*c)
			c += 1
			
			if world.maplist[self.pos[2]][self.on_map].npcs[yy][xx] == 0:
				screen.write_hit_matrix(xx,yy,1)
			elif world.maplist[self.pos[2]][self.on_map].npcs[yy][xx] != 0:#there is a monster here
				player.attack_monster(xx,yy,'magic')
				run = False
			
			if c > 4 or world.maplist[self.pos[2]][self.on_map].tilemap[yy][xx].transparency == False:
				run = False
				
				
	def respawn(self):
		
		self.pos[2] = 0
		self.pos[0] = world.startx
		self.pos[1] = world.starty
		self.on_map = 'local_0_0'
		
		self.xp = 0 #the player always lose all xp on dead
		self.lp = self.attribute.max_lp
		self.attribute.hunger = self.attribute.hunger_max
		self.attribute.thirst = self.attribute.thirst_max
		self.attribute.tiredness = self.attribute.tiredness_max
		self.buffs = buffs()
		
		if self.difficulty == 0:#the player plays on easy
			self.inventory.materials = materials()#reset materials
			if self.inventory.wearing['Hold(R)'].cursed == 0:
				self.inventory.wearing['Hold(R)'] = self.inventory.nothing
		elif self.difficulty == 1:#the player plays on normal
			self.inventory = inventory(5)#reset inventory
		elif self.difficulty == 2:#the player plays on hard
			self.inventory = inventory(5)#reset inventory
			self.lvl = 0#reset lvl
			self.attribute = attribute(2,2,2,2,2,10,10)#reset attribute
		elif self. difficulty == 3:#the player plays on Roguelike
			#del everything
			
			try:
				player_path = save_path + 'player.data'
				os.remove(player_path)
			except:
				None
									
			try:
				world_path = save_path + 'world.data'
				os.remove(world_path)
			except:
				None	
									
			try:
				gods_path = save_path + 'gods.data'
				os.remove(gods_path)
			except:
				None
									
			try:
				time_path = save_path + 'time.data'
				os.remove(time_path)
			except:
				None
		
		self.stand_check()
		
			
class messager():
	
	def __init__(self):
		self.mes_list = []
		self.last_mes = 'foo'
		self.mes_history = [[]]
		self.history_page = 0
		self.last_output = [' ',' ',' ',' ',' ']
		self.more_messages = False
		
	def add(self, new_message, check_if_new = False):
		# check_if_new is only needed by the (mob)player.stand_check function to prove there is only shown a new message about the ground when the player enters a new kind of ground
		if check_if_new == False:
			self.mes_list.append(new_message)
			self.mes_history[self.history_page].append(new_message)
			
			if len(self.mes_history[self.history_page]) == 7:
				self.mes_history.append([])
				if len(self.mes_history) > 10:
					del self.mes_history[0]
				else:
					self.history_page +=1
			
		elif check_if_new == True and self.last_mes != new_message:
			self.last_mes = new_message
			self.mes_list.append(new_message)
			
			self.mes_history[self.history_page].append(new_message)
			
			if len(self.mes_history[self.history_page]) == 7:
				self.mes_history.append([])
				if len(self.mes_history) > 10:
					del self.mes_history[0]
				else:
					self.history_page +=1
			
	def clear(self):
		
		if self.more_messages == False:
			self.mes_list = []
		
	def render_history(self):
		
		page = self.history_page
		run = True
		
		while run:
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))

			s.blit(bg,(0,0))

			text_string = '~Message History~ [Page(' + str(page+1) + ' of ' + str(len(self.mes_history)) +')]'
			text_image = screen.font.render(text_string,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			for i in range (0, len(self.mes_history[page])):
				mes_image = screen.font.render(self.mes_history[page][i],1,(0,0,0))
				if low_res == False:
					s.blit(mes_image,(5,100+i*25))#blit menu_items
				else:
					s.blit(mes_image,(5,46+i*25))#blit menu_items
			text = '['+key_name['ws']+'] - Turn page ['+key_name['x']+'] - leave'	
			text_image = screen.font.render(text,1,(255,255,255))
			if low_res == True:
				s.blit(text_image,(2,225))
			else:
				s.blit(text_image,(5,335))
			
			if game_options.mousepad == 1 and low_res == False:	
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			screen.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'w' or ui == 'a':
				page -= 1
				if page < 0:
					page = len(self.mes_history)-1
					
			if ui == 's' or ui == 'd':
				page += 1
				if page > len(self.mes_history)-1:
					page = 0
					
			if ui == 'x':
				run = False
			
	def sget(self):
		
		s_list = self.mes_list
		s_list.reverse()
		
		if len(self.mes_list) > 0:
				
			for c in range(0,5):
				s_list.append(' ')
			
			self.last_output = s_list	
		else:
			return self.last_output
				
		return s_list
		
class inventory():
	
	def __init__(self, equipment=7, food=7, misc=7):
		
		self.nothing = item_wear('Nothing',21,0,0)
		self.wearing = {'Head' : self.nothing, 'Body' : self.nothing, 'Legs' : self.nothing, 'Feet' : self.nothing, 'Hand' : self.nothing, 'Neck' : self.nothing, 'Hold(R)' : self.nothing, 'Hold(L)' : self.nothing, 'Background' : self.nothing, 'Clothing' : self.nothing, 'Hat' : self.nothing, 'Axe' : self.nothing, 'Pickaxe' : self.nothing}
		self.item_change = self.nothing
		self.equipment = []
		self.food = []
		self.misc = []
		self.materials = materials()
		self.blueprint = il.ilist['misc'][15]#a ordenary blueprint
		self.inv_mes = '~*~'
		
		for i in range (0,equipment):
			self.equipment.append(self.nothing)
		for i in range (0,food):
			self.food.append(self.nothing)
		for i in range (0,misc):
			self.misc.append(self.nothing)
			
		#go on here
	
	def wear(self, slot):
		
		if self.equipment[slot] != self.nothing:
		
			self.inv_mes = 'Now you wear a  %s.' %(self.equipment[slot].name)
		
			if self.wearing[self.equipment[slot].worn_at] != self.nothing and self.wearing[self.equipment[slot].worn_at].cursed != 0:
				self.item_change = self.wearing[self.equipment[slot].worn_at]
				self.wearing[self.equipment[slot].worn_at] = self.equipment[slot]
				self.equipment[slot] = self.item_change
				self.item_change = self.nothing
			elif self.wearing[self.equipment[slot].worn_at].cursed == 0:
				self.inv_mes = 'You can\'t! It\'s cursed!'
				self.wearing[self.equipment[slot].worn_at].identification()
			else:
				self.wearing[self.equipment[slot].worn_at] = self.equipment[slot]
				self.equipment[slot] = self.nothing
		
	def unwear(self, slot):
		
		worn = ['Hold(R)','Hold(L)','Head','Body','Legs','Feet','Hand','Neck','Axe','Pickaxe','Background','Clothing','Hat']	
		
		if self.wearing[worn[slot]].cursed != 0: #this is no cursed item
		
			num = -1
			found = -1
		
			for i in self.equipment:
			
				if found != -1:
					break
				
				num += 1
				if i == self.nothing:
					found = num
				
			if found > -1:
				self.equipment[num] = self.wearing[worn[slot]]
				self.inv_mes = 'You unwear a %s.' %( self.wearing[worn[slot]].name)
				self.wearing[worn[slot]] = self.nothing
			else:
				self.inv_mes = 'You have no free space in your inventory!'
		else: #this item is cursed
			
			self.inv_mes = 'You can\'t! It\'s cursed!'
			self.wearing[worn[slot]].identification()
			
	def drop(self,category, slot):
		
		worn = ['Hold(R)','Hold(L)','Head','Body','Legs','Feet','Hand','Neck','Axe','Pickaxe','Background','Clothing','Hat']
		
		try:
			field_full = False
			sacrifice = False
			
			string = 'foo'
			
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace != None and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID != tl.tlist['functional'][3].techID and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID != tl.tlist['functional'][4].techID and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID != tl.tlist['functional'][5].techID: #only at fields with empty ground the player can drop something. exeptions are full chests, empty chests and stacks. 
				field_full = True
				string = 'Not here!'
				
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][3].techID or world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][4].techID or world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][5].techID:
				if 	world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] != 0: #there are already things here
					if len(world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items) > 6:
						field_full = True
						string = 'There are already too many items at this place!'
			
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][15].techID:#this is a altar 
				field_full = False
				sacrifice = True
				
			if string != 'foo':
				self.inv_mes = string
			
		except: 
			field_full = False
			
		if category > 1 or self.wearing[worn[slot]].cursed != 0:#there is no worn cursed item you wanna drop
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].damage == 0 and field_full == False: #you only can drop thing on save tiles with 7 or less other items on it
			
				if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] == 0: #if there is no container
					world.maplist[player.pos[2]][player.on_map].add_container([self.nothing],player.pos[0],player.pos[1],False) #make new container
				
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID != tl.tlist['functional'][3].techID and sacrifice == False: #if there is no empty chest at this pos and this is no sacrifice make a stack
						help_tile = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]]) #get old tile at player pos
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['functional'][5]) #set new tile on player pos
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace = help_tile #set replace tile at the new position to the old tile at this pos
					elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][3].techID:
						replace = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace)
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['functional'][4])#else make a full chest out of the empty one
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace = replace
					
				if category == 0 or category == 1:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items.append(self.wearing[worn[slot]])
					if self.wearing[worn[slot]] != self.nothing: #this slot isn't empty
						self.inv_mes = 'You drop a %s.' %(self.wearing[worn[slot]].name)
					self.wearing[worn[slot]] = self.nothing
				elif category == 2:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items.append(self.equipment[slot])
					if self.equipment[slot] != self.nothing:
						self.inv_mes = 'You drop a %s.' %(self.equipment[slot].name)
					self.equipment[slot] = self.nothing
				elif category == 3:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items.append(self.food[slot])
					if self.food[slot] != self.nothing:
						self.inv_mes = 'You drop a %s.' %(self.food[slot].name)
					self.food[slot] = self.nothing
				elif category == 4:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items.append(self.misc[slot])
					if self.misc[slot] != self.nothing:
						self.inv_mes = 'You drop a %s.' %(self.misc[slot].name)
					self.misc[slot] = self.nothing
				
				for i in range (0, len(world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items)): #check for empty slots and errase them if necessary ---------- unsure because the -1
					try:#try-except is needed because the length of the list can change
						if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[i] == self.nothing:
							del world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[i]
					except:
						None
						
				if sacrifice == True:
					
					for j in range (0, len(world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items)):
						
						equipment = False
						food = False
						mood_change = 0
						
						try:
							# if this is working this must be a equipment item
							if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].state > 40:#this is equipment in a good state
								equipment = True
								if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'wooden':
									mood_change += 1
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'tin':
									mood_change += 2
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'copper':
									mood_change += 4
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'steel':
									mood_change += 6
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'titan':
									mood_change += 8
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'magnicum':
									mood_change += 10
						except:
							# if this is working this must be a food item
							if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].rotten == False: #this is unrotten food
								food = True
								mood_change += 2
								
								
						finally:
							 
							if equipment == False and food == False:
								mood_change = -1*(random.randint(1,10))
							
							if mood_change == 0:
								self.inv_mes = 'The gods accept your sacrifice.'
							elif mood_change > 0:
								self.inv_mes = 'The goods seem to be pleased...'
							else:
								self. inv_mes = 'It seems the gods dislike your gift...'
									 
							gods.mood += mood_change
							
							world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = 0 # del all sacrificed items 
								 
		else:#you try to drop a worn, cursed item
			
			self.inv_mes = 'You can\'t! It\'s cursed!'
			self.wearing[worn[slot]].identification()
		
	def use(self,slot):
		
		if self.misc[slot] != self.nothing:
			
			if self.misc[slot].use_name == 'place' or self.misc[slot].use_name == 'plant':
				
				if self.misc[slot].use_name == 'plant':
					grown_check = world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].can_grown
				else:
					grown_check = True
				
				if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace == None and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].damage == 0 and grown_check == True:
				
					replace = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]])
					world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist[self.misc[slot].place_cat][self.misc[slot].place_num])
					world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace = replace
					if self.misc[slot].use_name == 'plant':
						message.add('You planted a %s' %(self.misc[slot].name))
					else:
						message.add('You placed a %s' %(self.misc[slot].name))
					if self.misc[slot].name == 'Bomb':
						world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('bomb3',player.pos[0],player.pos[1],1))
					self.misc[slot] = self.nothing
					return True #if use returns a true this means after this action the inventory is closed. this action needs a turn
				else:
				
					self.inv_mes = 'Not here!'
					return False #this dosn't need a turn
			
			elif self.misc[slot].use_name == 'apply':#this is a blueprint. only blueprints are allowed to use 'apply'
				helpslot = player.inventory.blueprint
				player.inventory.blueprint = self.misc[slot]
				self.misc[slot] = helpslot
			
			elif self.misc[slot].name == 'Heart-Shaped Crystal':
				if player.attribute.max_lp < 20:
					if player.lp < player.attribute.max_lp:
						message.add('All your wounds are healed.')
					player.attribute.max_lp += 2
					player.lp = player.attribute.max_lp
					message.add('You feel more healthy now.')
				else:
					message.add('Nothing happens.')
				self.misc[slot] = self.nothing
				return True
			
			elif self.misc[slot].name == 'Mysterious Blue Crystal':
				if player.attribute.max_mp > 5:
					message.add('Your magic talents seem to grow.')
					player.attribute.max_mp -= 2
					if player.mp > player.attribute.max_mp:
						player.mp == player.attribute.max_mp
				else:
					message.add('Nothing happens.')
				self.misc[slot] = self.nothing
				return True
			
			elif self.misc[slot].name == 'Anchanted Enhancemen Powder':
				if self.wearing['Hold(R)'] != self.nothing:
					if self.wearing['Hold(R)'].plus < 2:
						mes = 'Your ' + self.wearing['Hold(R)'].name + ' glowes blue.'
						message.add(mes)
						self.wearing['Hold(R)'].plus += 1
						self.wearing['Hold(R)'].set_name()
						self.misc[slot] = self.nothing
					else:
						message.add('Nothing happens.')
					return True						
				else:
					self.inv_mes = 'You need to hold something inside your hand to use this.'
			
			elif self.misc[slot].name == 'Heavy Bag':
				message.add('You open the bag.')
				if self.materials.wood < self.materials.wood_max:
					wood_num = random.randint(1,9)
				else:
					wood_num = 0
				if self.materials.stone < self.materials.stone_max:
					stone_num = random.randint(1,9)
				else:
					stone_num = 0
				if self.materials.ore < self.materials.ore_max:
					ore_num = random.randint(-3,3)
					if ore_num < 0:
						ore_num = 0
				else:
					ore_num = 0
				if self.materials.gem < self.materials.gem_max:
					gem_num = random.randint(-6,2)
					if gem_num < 0:
						gem_num = 0
				else:
					gem_num = 0
				
				string = 'It contains: ' + str(wood_num) + ' wood, ' +str(stone_num) + ' stone'
				
				if ore_num > 0:
					string = string + ', ' + str(ore_num) + ' ore'
				if gem_num > 0:
					string = string + ', ' + str(gem_num) + ' gem'
					
				wood_num = self.materials.add('wood', wood_num)
				stone_num = self.materials.add('stone', stone_num)
				ore_num = self.materials.add('ore', ore_num)
				gem_num = self.materials.add('gem', gem_num)
				
				string = ''
				
				if wood_num != 'Full!':
					string = string + str(wood_num)
				if stone_num != 'Full!':	 
					string = string + ',' + str(stone_num)
				if ore_num != 'Full!':
					string = string + ',' + str(ore_num)
				if gem_num != 'Full!':
					string = string + ',' + str(gem_num)
					
				if wood_num+stone_num+ore_num+gem_num == 0:
					string = 'Your bags are to full to keep anything out of the bag.'
					
				message.add(string)
				
				self.misc[slot] = self.nothing
				
				return True
			
			elif self.misc[slot].use_name == 'read':#this is a scroll or a spellbook
				
				if self.misc[slot].name.count('Scroll') > 0:
					scroll = True
				else:
					scroll = False
					
				if player.mp < player.attribute.max_mp and scroll == False:
					self.inv_mes = 'You are not focused.'
					return False #this dosnt need a turn
					
				if self.misc[slot].effect == 0: #identify
					
					bodyparts = ('Head','Body','Legs','Feet','Hand','Neck','Hold(R)', 'Hold(L)')
					
					for i in bodyparts:
						if self.wearing[i] != self.nothing:
							self.wearing[i].identification()
							
					for j in range(0,len(self.equipment)):
						if self.equipment[j] != self.nothing:
							self.equipment[j].identification()
						
					message.add('Now you aware about your equipment\'s states.')
						
				elif self.misc[slot].effect == 1: #repair
					
					bodyparts = ('Head','Body','Legs','Feet','Hand','Neck','Hold(R)','Hold(L)')
					final_bodyparts = []
					
					for i in bodyparts:
						
						if self.wearing[i] != self.nothing and self.wearing[i].state != 0:
							final_bodyparts.append(i)
							
					if len(final_bodyparts) != 0:	
						ran = random.randint(0, len(final_bodyparts)-1) # select a random item for repair, migt be replaced just with zero
						# select the most damaged equipped inventory item
						for i in range(0,len(final_bodyparts)):
							if self.wearing[final_bodyparts[i]].state<self.wearing[final_bodyparts[ran]].state:
								ran = i
						self.wearing[final_bodyparts[ran]].state = 100 # actually repair the item
						self.wearing[final_bodyparts[ran]].set_name() # and reset its name accordingly
						mes = 'Your ' + self.wearing[final_bodyparts[ran]].classe + ' '
						if final_bodyparts[ran] == 'Feet':
							mes = mes + 'are'
						else:
							mes = mes + 'is'
						mes = mes + ' fully repaired now.'
						message.add(mes)
					else:
						message.add('Nothing seems to happen.')
						
				elif self.misc[slot].effect == 2: #healing
					
					if player.lp < player.attribute.max_lp:
						player.lp = player.attribute.max_lp
						message.add('Your wounds heal immediately.')
					else:
						message.add('Nothing seems to happen.')
						
				elif self.misc[slot].effect == 3: #teleport
					
					pos_list = world.maplist[player.pos[2]][player.on_map].find_all_moveable(False)
					
					if len(pos_list) > 1:
						ran = random.randint(0,len(pos_list)-1)
						pos = pos_list[ran]
						player.pos[0] = pos[0]
						player.pos[1] = pos[1]
						player.stand_check()
						message.add('You teleport your self.')
					else:
						message.add('Nothing seems to happen')
					
						
				elif self.misc[slot].effect == 4:#return
					
					if player.pos[0] != world.startx or player.pos[1] != world.starty or player.pos[2] != 0:
						player.pos[0] = world.startx
						player.pos[1] = world.starty
						player.pos[2] = 0
						player.on_map = 'local_0_0'
						message.add('You returne home.')
					else:
						message.add('Nothing seems to happen.')

				elif self.misc[slot].effect == 5: #flames
					
					num_flames = 0
					
					for y in range(player.pos[1]-1,player.pos[1]+2):
						for x in range(player.pos[0]-1,player.pos[0]+2):
							
							if x != player.pos[0] or y !=player.pos[1]:
								if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace == None and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'solide':
									replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x]
									world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tl.tlist['effect'][4])
									world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = replace
									world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('flame',x,y,2))
									num_flames+=1
									if world.maplist[player.pos[2]][player.on_map].npcs[y][x] != 0:
										try:
											world.maplist[player.pos[2]][player.on_map].npcs[y][x].lp -=3
											if world.maplist[player.pos[2]][player.on_map].npcs[y][x].lp < 1:
												world.maplist[player.pos[2]][player.on_map].monster_die(x,y)
												world.maplist[player.pos[2]][player.on_map].make_monsters_angry(x,y,'kill')
										except:
											None
								
					if num_flames != 0:
						message.add('Magical flames start to burn close to you.')
					else:
						message.add('Nothing seems to happen.')
				
				elif self.misc[slot].effect == 6:#healing aura
					
					num_aura = 0
					
					for y in range(player.pos[1]-1,player.pos[1]+2):
						for x in range(player.pos[0]-1,player.pos[0]+2):
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace == None and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'solide' and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].damage == False:
								replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x]
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tl.tlist['effect'][5])
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = replace
								world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('healing_aura',x,y,10))
								num_aura+=1
								
					if num_aura != 0:
						message.add('A healing aura spreades under your feet.')
					else:
						message.add('Nothing seems to happen.')
				
				elif self.misc[slot].effect == 7:
					player.buffs.set_buff('light',180)
					message.add('A magical light surrounds your body.')
					player.stand_check()
				
				if scroll == True:
					self.misc[slot] = self.nothing
					message.add('The scroll turns to dust.')
				else:
					player.mp = 0
					message.add('You lose your focus.')
				
				return True
			
			elif self.misc[slot].name == 'Chalk':
				
				x = player.pos[0]
				y = player.pos[1]
				
				if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace == None:
					replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x]
					world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tl.tlist['effect'][6])
					world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = replace
					duration = random.randint(10,30)
					world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('elbereth',x,y,duration))
					message.add('You write the magic word on the ground.')
					
					breaking = random.randint(0,99)
					if breaking < 11:
						message.add('The chalk breaks.')
						self.misc[slot] = self.nothing
					
					return True
				else:
					self.inv_mes = 'Not here!'
					return False
				
			elif self.misc[slot].name == 'Fishing rod':
				
				chance = 0 
				
				for y in range (player.pos[1]-1, player.pos[1]+1):
					for x in range (player.pos[0]-1, player.pos[0]+1):
						
						if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['misc'][0].techID: #this is low water
							chance += 1
						elif world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['misc'][3].techID: #this is water
							chance += 2
						
				if chance == 0:
					self.inv_mes ='Not here!'
					return False
				
				run = True
				
				while run:
					got_fish = random.randint(0,20)
					
					if chance > got_fish:
						status_quo = world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] #save the container at this ülace
						coin = random.randint(0,99)
					
						if coin < 75:
						
							items = (il.ilist['food'][4],il.ilist['food'][25])#catch a fish or a jellyfish
						
							choose = random.randint(0,len(items)-1)
						
							world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = container([items[choose]])#set a temporary container
							test = world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].loot(0)
						
							if test == True:
								message.add('You got a ' + items[choose].name + '.')
								screen.write_hit_matrix(player.pos[0],player.pos[1],10)
								sfx.play('got_fish')
							else:
								message.add('You got a ' + items[choose].name + ', but you can\'t keep it.')
								sfx.play('got_fish')
							
						else:
							#catch old shoes
							material = random.randint(6,20) #no wooden shoes. they would swim ;-)
							curse = random.randint(0,2)
							plus = random.randint(-2,2)
							state = random.randint(4,11)
						
							item = item_wear('shoes',material,plus,state,curse)
						
							world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = container([item])
							test = world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].loot(0)
							
							if test == True:
								message.add('You got some old ' + item.name + '.')
								screen.write_hit_matrix(player.pos[0],player.pos[1],11)
								sfx.play('got_fish')
							else:
								message.add('You got some old ' + item.name + ', but you can\'t keep it.')
								sfx.play('got_fish')
							
						world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = status_quo #recover the old container 
					
					else:
						message.add('It seems nothing want to bite...')
						sfx.play('no_fish')
					
					for yy in range(player.pos[1]-1,player.pos[1]+2):
						for xx in range(player.pos[0]-1,player.pos[0]+2):
							
							if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx] != 0:
								message.add('A monster interrupts you!')
								return True
					
					screen.render_request('['+key_name['e']+']-Go on!',' ','['+key_name['x']+']-Stop')
					
					run2 = True
					
					while run2:
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
					
						if ui == 'e':
							time.tick()
							screen.reset_hit_matrix()
							run2 = False
						elif ui == 'x':
							run = False
							run2 = False
				return True
				
			elif self.misc[slot].name == 'Torch':
				
				player.buffs.set_buff('light',180)
				self.misc[slot] = self.nothing
				message.add('The burning torch illumines your surroundings.')
				player.stand_check()
				return True
							
	def eat(self,slot):
		
		if self.food[slot] != self.nothing:
			
			player.attribute.hunger += self.food[slot].satisfy_hunger
			if player.attribute.hunger > player.attribute.hunger_max:
				player.attribute.hunger = player.attribute.hunger_max+1 #the +1 is because the attribute will fall one point at the same turn
			
			player.attribute.thirst += self.food[slot].satisfy_thirst
			if player.attribute.thirst > player.attribute.thirst_max:
				player.attribute.thirst = player.attribute.thirst_max+1 #the +1 is because the attribute will fall one point at the same turn
			
			
			player.buffs.set_buff('adrenalised',self.food[slot].satisfy_tiredness)
			
			player.lp += self.food[slot].heal
			if player.lp > player.attribute.max_lp:
				player.lp = player.attribute.max_lp
			
			player.attribute.hunger_max += self.food[slot].rise_hunger_max
			player.attribute.thirst_max += self.food[slot].rise_thirst_max	
			player.attribute.tiredness_max += self.food[slot].rise_tiredness_max
			player.attribute.max_lp += self.food[slot].rise_lp_max
			
			player.inventory.materials.add('seeds', self.food[slot].give_seed)
			
			if self.food[slot].rotten == False:
				self.inv_mes = self.food[slot].eat_mes
			else:
				blind_coin = random.randint(0,1)
				if blind_coin == 1:
					blind_dur = random.randint(60,180)
					player.buffs.set_buff('blind',blind_dur)
					
				poison_coin = random.randint(0,1)
				if poison_coin == 1:
					posion_dur = random.randint(60,240)
					player.buffs.set_buff('poisoned',posion_dur)
					
				self.inv_mes = 'BAH! Rotten food...'
			
			self.food[slot] = self.nothing
			
	def render(self, category, slot, info=False):
		
		test = True
		
		s = pygame.Surface((640,360))
		
		if category != 1:
			s.blit(gra_files.gdic['display'][1],(0,0)) #render background
		else:
			if low_res == False:
				s.blit(gra_files.gdic['display'][49],(0,0))
			else:
				s.blit(gra_files.gdic['display'][50],(0,0))
		
		if low_res == False:
			text_y = 120
			marker_y = 115
		else:
			text_y = 60
			marker_y = 52
		
		num = 0
		if low_res == False:
			text = '~Inventory~ [Press ['+key_name['x']+'] to leave]'
		else:
			if self.inv_mes == '~*~':
				text = '~Inventory~ [Press ['+key_name['x']+'] to leave]'
			else:
				text =self.inv_mes
				
		text_image = screen.font.render(text,1,(255,255,255))
		s.blit(text_image,(5,2))#menue title
		
		for c in range(0,6):
			s.blit(gra_files.gdic['display'][2],(c*50,25))#blit empty tabs
			
		s.blit(gra_files.gdic['display'][3],(category*50,25))#blit used tab
		
		tab_names = ('Worn1','Worn2','Equi.','Food','Misc', 'Reso.')
		
		for d in range (0,6):
			
			text_image = screen.font.render(tab_names[d],1,(0,0,0))
			s.blit(text_image,(d*50+5,27))#blit tb names
			
		if category == 0 or category == 1:
			
			if category == 0:
				h = ['Hold(R)','Hold(L)','Head','Body','Legs','Feet','Hand','Neck']
			else:
				h = ['Axe','Pickaxe','Background','Clothing','Hat']
				
			s.blit(gra_files.gdic['display'][4],(0,marker_y+slot*23))#blit marker
			 
			for i in h:
				
				color = (0,0,0)
				
				if self.wearing[i] != self.nothing: 
					if self.wearing[i].known == True:
						if self.wearing[i].cursed < 1:#cursed item
							color = (130,0,190)
						elif self.wearing[i].cursed > 1:#holy item
							color = (100,115,0)
					if self.wearing[i].state < 11:
						color = (200,0,0)
				else:
					if i == h[slot]:
						test = False
				
				string = i + ' : ' + self.wearing[i].name
				text_image = screen.font.render(string,1,color)
				s.blit(text_image,(21,text_y+num*23))#blit item names
				
				num += 1
			
		elif category == 2:
			
			for i in self.equipment:
				
				color = (0,0,0)
				
				if i != self.nothing: 
					if i.known == True:
						if i.cursed < 1:#cursed item
							color = (130,0,190)
						elif i.cursed > 1:#holy item
							color = (100,115,0)
					if i.state < 11:
						color = (200,0,0)
		
				
				if slot == num:
					s.blit(gra_files.gdic['display'][4],(0,marker_y+num*25))#blit marker
				
				if self.equipment[slot] == self.nothing:
					test = False
				
				text_image = screen.font.render(i.name,1,color)
				s.blit(text_image,(21,text_y+num*25))#blit item names
			
				num += 1
		
		elif category == 3:
			
			for i in self.food:
				
				color = (0,0,0)
				
				if i != self.nothing:
					if i.rotten == True:
						color = (200,0,0)
			
				if slot == num:
					s.blit(gra_files.gdic['display'][4],(0,marker_y+num*25))#blit marker
				
				if self.food[slot] == self.nothing:
					test = False
				
				text_image = screen.font.render(i.name,1,color)
				s.blit(text_image,(21,text_y+num*25))#blit item names
				
				num += 1
				
		elif category == 4:
			
			for i in self.misc:
				
				if self.misc == self.nothing:
					use_name = False
				
				if slot == num:
					s.blit(gra_files.gdic['display'][4],(0,marker_y+num*25))#blit marker
				
				text_image = screen.font.render(i.name,1,(0,0,0))
				s.blit(text_image,(21,text_y+num*25))#blit item names
			
				num += 1
		
		elif category == 5:
			
			string = 'Wood: ' + str(self.materials.wood) + '/' + str(self.materials.wood_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y))#blit wood line
			
			string = 'Stone: ' + str(self.materials.stone) + '/' + str(self.materials.stone_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+25))#blit stone line
			
			string = 'Ore: ' + str(self.materials.ore) + '/' + str(self.materials.ore_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+50))#blit ore line
			
			string = 'Herbs: ' + str(self.materials.herb) + '/' + str(self.materials.herb_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+75))#blit herbs line
			
			string = 'Gem: ' + str(self.materials.gem) + '/' + str(self.materials.gem_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+100))#blit gem line
		
			string = 'Seeds: ' + str(self.materials.seeds) + '/' + str(self.materials.seeds_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+125))#blit gem line
			
			string = 'Built with: ' + player.inventory.blueprint.name 
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+160))#blit blueprint line
		
		text_image = screen.font.render(self.inv_mes,1,(255,255,255))
		s.blit(text_image,(5,335))
		self.inv_mes = '~*~'
		
		if info == True:
			s.blit(gra_files.gdic['display'][5],(0,0))
			
			use_name = 'use'
			if category == 0 or category == 1:
				use_name = 'unequip'
			elif category == 2:
				use_name = 'equip'
			elif category == 3:
				use_name = self.food[slot].eat_name
			elif category == 4:
				use_name = self.misc[slot].use_name
				
			drop_name = 'drop'
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][15]: #this is an altar
				drop_name = 'sacrifice'
			elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][3] or world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][4]:
				drop_name = 'store'
			#Add trash here
			
			use_image = screen.font.render('['+key_name['e']+'] - '+use_name,1,(255,255,255))
			s.blit(use_image,(5,0))
			drop_image = screen.font.render('['+key_name['b']+'] - '+drop_name,1,(255,255,255))
			s.blit(drop_image,(5,15))
			info_image = screen.font.render('['+key_name['i']+'] - info',1,(255,255,255))
			s.blit(info_image,(5,30))
			cancel_image = screen.font.render('['+key_name['x']+'] - cancel',1,(255,255,255))
			s.blit(cancel_image,(5,45))
		
		if game_options.mousepad == 1 and low_res == False:
			s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
		else:
			s_help = pygame.Surface((160,360))
			s_help.fill((48,48,48))
			s.blit(s_help,(480,0))
		
		if game_options.mousepad == 0 and low_res == False:
			s_help = pygame.Surface((640,360))
			s_help.fill((48,48,48))
			s_help.blit(s,(80,0))
			s = s_help
		if low_res == False:
			s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
		
		screen.screen.blit(s,(0,0))
		
		pygame.display.flip()
		
		return test
				
	def inv_user_interaction(self):
		
		run = True
		category = 0
		slot = 0
		info = False
		worn = ['Hold(R)','Hold(L)','Head','Body','Legs','Feet','Hand','Neck','Axe','Pickaxe','Background','Clothing','Hat']
		
		while run:
			try:
				master_test = self.render(category, slot, info)
			except:
				master_test = False
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'd' and info == False:	
				slot = 0
				category += 1
				if category > 5: ######change######
					category = 0
			elif ui == 'a' and info == False:
				slot = 0
				category -= 1
				if category < 0: ######change######
					category = 5
			elif ui == 'x' and info == False:
				run = False
				break
			elif ui == 'x' and info == True:
				info = False
			elif ui == 'w' and info == False:
				slot -= 1
				if category == 0:
					if slot < 0:
						slot = 7
				elif category == 2:
					if slot < 0:
						slot = len(self.equipment)-1
				elif category == 3:
					if slot < 0:
						slot = len(self.food)-1
				elif category == 4:
					if slot < 0:
						slot = len(self.misc)-1
				elif category == 1:
					if slot < 0:
						slot  = 4
						
			elif ui == 's' and info == False:
				slot += 1
				if category == 0:
					if slot == 8:
						slot = 0
				elif category == 2:
					if slot == len(self.equipment):
						slot = 0
				elif category == 3:
					if slot == len(self.food):
						slot = 0
				elif category == 4:
					if slot == len(self.misc):
						slot = 0
				elif category == 1:
					if slot > 4:
						slot = 0
						
			elif ui == 'e' and info == True:
				
				if category == 0 and self.wearing[worn[slot]] != self.nothing:
					self.unwear(slot)
				elif category == 2:
					self.wear(slot)
				elif category == 3:
					self.eat(slot)
				elif category == 4:
					test = self.use(slot)
					if test == True:
						run = False
				elif category == 1 and self.wearing[worn[slot+8]] != self.nothing:
					self.unwear(slot+8)
				
				info = False
					
			elif ui == 'e' and info == False and master_test == True and category != 5:
				info = True
						
			elif ui == 'b':
				
				drop_test =  True
				if category == 0:
					if self.wearing[worn[slot]] == self.nothing:
						drop_test = False
				elif category == 2:
					if self.equipment[slot] == self.nothing:
						drop_test = False
				elif category == 3:
					if self.food[slot] == self.nothing:
						drop_test = False
				elif category == 4:
					if self.misc[slot] == self.nothing:
						drop_test = False
				elif category == 5:
					drop_test = False
				elif category == 1:
					if self.wearing[worn[slot+8]] == self.nothing:
						drop_test = False
						
				if drop_test == True:
					if category != 1:
						self.drop(category,slot)
					else:
						self.drop(0,slot+8)
				info = False
			
			elif ui == 'i' and info == True:
				
				static_txt = True
				
				if category == 0:
					txt = self.wearing[worn[slot]].classe
				elif category == 2:
					if self.equipment[slot].name.find('[D]') != -1:#this is decorative clothing
						txt = 'decorative_clothes'
					else:
						txt = self.equipment[slot].classe
				elif category == 1:
					if self.wearing[worn[slot+8]].name.find('[D]') != -1:
						txt = 'decorative_clothes'
					else:
						txt = self.wearing[worn[slot+8]].classe
				elif category == 3:
					static_txt = False
					txt = []
					txt.append(self.food[slot].name)
					txt.append(' ')
					if self.food[slot].satisfy_hunger > 0:
						txt.append('Reduces hunger.')
					if self.food[slot].satisfy_hunger < 0:
						txt.append('Raises hunger.')
					if self.food[slot].satisfy_thirst > 0:
						txt.append('Reduces thirst.')
					if self.food[slot].satisfy_thirst < 0:
						txt.append('Raises thirst.')
					if self.food[slot].satisfy_tiredness > 0:
						txt.append('Can adrenalise!')
					if self.food[slot].rise_hunger_max > 0:
						txt.append('Let your stomach grow.')
					if self.food[slot].rise_thirst_max > 0:
						txt.append('Raises your water capacity.')
					if self.food[slot].rise_tiredness_max > 0:
						txt.append('Raises your sleep capacity.')#I'm not happy with this phrase
					if self.food[slot].heal > 0:
						txt.append('Can heal your wounds.')
					if self.food[slot].heal > 0:
						txt.append('Can hurt you!')
					if self.food[slot].rise_lp_max > 0:
						txt.append('Raises your max. LP.')
					if self.food[slot].rotten:
						txt.append('Rotten food may harm you!.')
				elif category == 4:
					if self.misc[slot].name.find('Blueprint') != -1:
						txt = 'Blueprint'
					elif self.misc[slot].name.find('Scroll') != -1:
						txt = 'Scroll'
					elif self.misc[slot].name.find('Spellbook') != -1:
						txt = 'Spellbook'
					else:
						if texts[self.misc[slot].name]:
							txt = self.misc[slot].name
						else:
							txt = 'info_soon' 	
				
				else:
					txt = 'info_soon'
				
				if static_txt:	
					t = screen.render_text(texts[txt])
				else:
					t = screen.render_text(txt)
					
				info = False
				
				if t == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
		
class container():
	
	def __init__(self, items, deep_copy = True):
		
		if deep_copy:
			self.items = deepcopy(items)
		else:
			self.items = items
		self.con_mes = '~*~'
					
	def loot(self,num,real_mes= False):
		
		if self.items[num].inv_slot == 'equipment':
			
			found_place = False
			
			for i in range (0, len(player.inventory.equipment)):
				
				if found_place != True:
					if player.inventory.equipment[i] == player.inventory.nothing:
						player.inventory.equipment[i] = self.items[num]
						self.con_mes = 'You looted a %s.' %(self.items[num].name)
						if real_mes == True:
							message.add('You looted a %s.' %(self.items[num].name))
						del self.items[num]
						found_place = True
			
		elif self.items[num].inv_slot == 'food':
			
			found_place = False
			
			for i in range (0, len(player.inventory.food)):
				
				if found_place != True:
					if player.inventory.food[i] == player.inventory.nothing:
						player.inventory.food[i] = self.items[num]
						self.con_mes = 'You looted a %s.' %(self.items[num].name)
						if real_mes == True:
							message.add('You looted a %s.' %(self.items[num].name))
						del self.items[num]
						found_place = True
		
		elif self.items[num].inv_slot == 'misc':
			
			found_place = False
			
			for i in range (0, len(player.inventory.misc)):
				
				if found_place != True:
					if player.inventory.misc[i]  == player.inventory.nothing:
						player.inventory.misc[i]  = self.items[num]
						self.con_mes = 'You looted a %s.' %(self.items[num].name)
						if real_mes == True:
							message.add('You looted a %s.' %(self.items[num].name))
						del self.items[num]
						found_place = True
		
		return found_place
						
	def inventory(self, tile_change = True):
		
		sfx.play('loot')
		
		run = True
		
		while run:
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
			
			running = True
			
			num = 0
			
			self.con_mes = '~*~'
			
			while running:
				
				if low_res == False:
					s = pygame.Surface((640,360))
				else:
					s = pygame.Surface((320,240))
				
				bg = pygame.Surface((480,360))
				bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
				if low_res == True:
					bg = pygame.transform.scale(bg,(320,240))

				s.blit(bg,(0,0))
			
				text = '~Loot~ [Press ['+key_name['x']+'] to leave]'
				text_image = screen.font.render(text,1,(255,255,255))
				s.blit(text_image,(5,2))#menue title
			
				for i in range (0,len(self.items)):
					
					color = (0,0,0)
					
					if self.items[i].inv_slot == 'equipment':
						if self.items[i].known == True:
							if self.items[i].cursed < 1:#cursed item
								color = (130,0,190)
							elif self.items[i].cursed > 1:#holy item
								color = (100,115,0)
						if self.items[i].state < 11:
							color = (200,0,0)
					elif self.items[i].inv_slot == 'food':
						if self.items[i].rotten == True:
							color = (200,0,0)
					
					if i == num:
						
						if low_res == False:
							s.blit(gra_files.gdic['display'][4],(0,112+num*25))#blit marker
						else:
							s.blit(gra_files.gdic['display'][4],(0,38+num*25))#blit marker
						
						text_string = self.items[i].name + '>['+key_name['e']+']loot'
						text_image = screen.font.render(text_string,1,color)
						if low_res == False:
							s.blit(text_image,(21,120+i*25))#blit menu_items
						else:
							s.blit(text_image,(21,46+i*25))#blit menu_items
							
					else:
						text_image = screen.font.render(self.items[i].name,1,color)
						if low_res == False:
							s.blit(text_image,(21,120+i*25))#blit menu_items
						else:
							s.blit(text_image,(21,46+i*25))#blit menu_items
				
				text_image = screen.font.render(self.con_mes,1,(255,255,255))
				if low_res == True:
					s.blit(text_image,(2,225))
				else:
					s.blit(text_image,(5,335))
				
				if game_options.mousepad == 1 and low_res == False:
					s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
				else:
					s_help = pygame.Surface((160,360))
					s_help.fill((48,48,48))
					s.blit(s_help,(480,0))
				
				if game_options.mousepad == 0 and low_res == False:
					s_help = pygame.Surface((640,360))
					s_help.fill((48,48,48))
					s_help.blit(s,(80,0))
					s = s_help
				
				if low_res == False:
					s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
				
				screen.screen.blit(s,(0,0))
				
				pygame.display.flip()
			
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					global player
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'x':
					running = False
					run = False
				elif ui == 'e':
					item_num = len(self.items)
					self.loot(num)
					if item_num > len(self.items):
						self.con_mes = '~*~'
						num = 0
					else:
						self.con_mes = 'You can\'t loot this...'
				elif ui == 'w':
					self.con_mes = '~*~'
					num -=1
					if num < 0:
						num = len(self.items)-1
				elif ui == 's':
					self.con_mes = '~*~'
					num += 1
					if num > len(self.items)-1:
						num = 0  
					
				if len(self.items) == 0 and tile_change == True:
					
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID != tl.tlist['functional'][4].techID:#this is no chest
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace
					else:
						replace = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace)
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['functional'][3])
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace = replace
						
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = 0
					message.add('You looted everything.')
					run = False
					break
					
				elif len(self.items) == 0:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = 0
					message.add('You looted everything.')
					run = False
					break

class time_class():
	
	def __init__(self):
		
		name = save_path + os.sep + 'time.data'
		Time_ready = True
		
		try:
			
			f = open(name, 'rb')
			screen.render_load(6)
			temp = p.load(f)
			self.minute = temp.minute
			self.hour = temp.hour
			self.day = temp.day
			self.day_total = temp.day_total
			self.month = temp.month
			self.year = temp.year
			
		except:
			
			screen.render_load(8)
			
			self.minute = 0
			self.hour = 6
			self.day = 1
			self.day_total = 0
			self.month = 1
			self.year = 1
		
	def tick(self):
		
		Time_ready = True

		for i in range (0,len(world.maplist[player.pos[2]][player.on_map].countdowns)): # check for countdown events
			
			if world.maplist[player.pos[2]][player.on_map].countdowns[i].x != player.pos[0] or world.maplist[player.pos[2]][player.on_map].countdowns[i].y != player.pos[1]:
				if world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]][player.pos[1]] == 0: #if there is no player or npc on the same tile like the countdown event
					test = world.maplist[player.pos[2]][player.on_map].countdowns[i].countdown()
			
					if test == True:
				
						if world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'door':
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = tl.tlist['building'][3]
							message.add('A door falls shut.')
							sfx.play('locked')
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'bomb3':
							replace =  world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = tl.tlist['effect'][1]
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace = replace
							world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('bomb2', world.maplist[player.pos[2]][player.on_map].countdowns[i].x, world.maplist[player.pos[2]][player.on_map].countdowns[i].y,1))
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'bomb2':
							replace =  world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = tl.tlist['effect'][2]
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace = replace
							world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('bomb1', world.maplist[player.pos[2]][player.on_map].countdowns[i].x, world.maplist[player.pos[2]][player.on_map].countdowns[i].y,1))
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'bomb1':
							
							for yy in range(world.maplist[player.pos[2]][player.on_map].countdowns[i].y-1,world.maplist[player.pos[2]][player.on_map].countdowns[i].y+2):
								for xx in range(world.maplist[player.pos[2]][player.on_map].countdowns[i].x-1,world.maplist[player.pos[2]][player.on_map].countdowns[i].x+2):
									
									if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx] != 0:
										world.maplist[player.pos[2]][player.on_map].npcs[yy][xx].lp -= 5
										if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx].lp < 1:
											world.maplist[player.pos[2]][player.on_map].monster_die(xx,yy)
									world.maplist[player.pos[2]][player.on_map].containers[yy][xx] = 0
									world.maplist[player.pos[2]][player.on_map].make_monsters_angry(xx,yy,'destroy')
									
									if player.pos[0] == xx and player.pos[1] == yy:
										player.lp -= 5
									
									if world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].replace != None:
										replace =  deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].replace)
									else:
										replace =  deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx])
										
									world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx] = deepcopy(tl.tlist['effect'][3])
									world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].replace = deepcopy(replace)
									world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('boom', xx, yy,1))
							
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							message.add('BOOOM!')
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'boom':
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'flame':
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'healing_aura' or world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'elbereth':
							if world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'elbereth':
								message.add('The magic word fades.')
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'		
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'init_tutorial':
							screen.render_text(texts['tutorial_1.1'])
							screen.render_text(texts['tutorial_1.2'])
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'spawner':
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							map_type = world.maplist[player.pos[2]][player.on_map].map_type
							
							spawn_here = False
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group == 'soil':
								spawn_here = True
							if map_type == 'grot':
								if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group == 'low_liquid':
									spawn_here = True
							
							if world.maplist[player.pos[2]][player.on_map].npcs[y][x] == 0:
								no_monsters = True
							else:
								no_monsters = False
							
							player_distance = ((player.pos[0]-x)**2+(player.pos[1]-y)**2)**0.5
							
							monster_max = (max_map_size*max_map_size)/30
							#monster_max = int(monster_max * world.maplist[player.pos[2]][player.on_map].monster_num)
							
							if world.maplist[player.pos[2]][player.on_map].monster_count < monster_max:
								if player_distance > 8:
									if spawn_here == True and no_monsters == True:
										ran = random.randint(0,len(ml.mlist[map_type])-1)
										world.maplist[player.pos[2]][player.on_map].npcs[y][x] = deepcopy(ml.mlist[map_type][ran])
										world.maplist[player.pos[2]][player.on_map].set_monster_strength(x,y,player.pos[2])
										try:
											if player.difficulty == 4:
												self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]].AI_style = 'ignore'
										except:
											None
										print(world.maplist[player.pos[2]][player.on_map].npcs[y][x].name, (x,y), str(world.maplist[player.pos[2]][player.on_map].monster_count)+'/'+str(monster_max))
										world.maplist[player.pos[2]][player.on_map].monster_count += 1
							world.maplist[player.pos[2]][player.on_map].countdowns[i].countfrom = random.randint(5,60)
						
							
		newcountdown = []
		
		for k in world.maplist[player.pos[2]][player.on_map].countdowns:
			if k != 'del':
				newcountdown.append(k)
				
		world.maplist[player.pos[2]][player.on_map].countdowns = newcountdown
		
		self.minute += 1
		
		if self.hour > 6 and self.hour < 20:
			thirst_multi = world.maplist[player.pos[2]][player.on_map].thirst_multi_day
		else:
			thirst_multi = world.maplist[player.pos[2]][player.on_map].thirst_multi_night
		
		if player.buffs.hexed <= 0:
			change = 1
		else:
			change = 5
			
		if player.buffs.poisoned > 0:
			change = 2
			
		if player.attribute.hunger > 0:
			player.attribute.hunger -= change
		if player.attribute.thirst > 0:	
			player.attribute.thirst -= change * thirst_multi
		if player.attribute.tiredness > 0 and player.buffs.adrenalised <= 0:
			player.attribute.tiredness -= change
		
		if player.attribute.hunger <= 0 or player.attribute.thirst <= 0 or player.attribute.tiredness <= 0:
			player.lp -= 1
			
		if self.minute % 5 == 0:#every 5th turn
			
			if player.buffs.bleeding <= 0 and player.buffs.poisoned <= 0 and player.lp < player.attribute.max_lp:
				player.lp += 1
			elif player.buffs.bleeding > 0:
				player.lp -= 1
				
			if player.buffs.confused <= 0:
				if player.mp < player.attribute.max_mp:
					player.mp += 1
					if player.mp == player.attribute.max_mp:
						message.add('You are focused again.') 
			else:
				player.mp = 0
				
		player.buffs.buff_tick()
		
		world.maplist[player.pos[2]][player.on_map].AI_move()
		
		if self.minute > 59:
			
			self.hour += 1
			self.minute = 0
			
			if self.hour > 23:
				
				self.day += 1
				self.day_total +=1
				self.hour = 0
				screen.render_load(5)
				save(world,player,time,gods,save_path,os.sep)#save the game
				
				if self.day > 28:
						
					self.month += 1
					self.day = 1
						
					if self.month > 13:
							
						self.year +=1
						self.month = 1
						self.day_total = 0 #eventually will cause a little bug when the year is changing but prevent the number of total days of become endless big
						
						if self.year > 9999:
							self.year = 0 #just to be save ;-)

	def sget(self):
		
		monthnames = ('None', 'Prim', 'Secut', 'Trilus', 'Quarz', 'Vivis', 'Sis', 'Septur', 'Huiles', 'Neurat', 'Dixa', 'Seprim', 'Tweflaf', 'Dritum')
		
		if self.day == 1:
			daystring = '1st'
		elif self.day == 2:
			daystring = '2nd'
		else:
			daystring = str(self.day) + 'th'
			
		if self.hour > 11:
			hourstring = str(self.hour-12)
			ampmstring = 'PM'
		else:
			hourstring = str(self.hour)
			ampmstring = 'AM'	
			
		if len(hourstring) == 1:
			hourstring = '0' + hourstring

		if hourstring == '00':
			hourstring = '12'
			
		if len(str(self.minute)) == 1:
			minutestring = '0' + str(self.minute)
		else:
			minutestring = str(self.minute)	
		
		date = daystring + ' ' + monthnames[self.month]
		time = hourstring + ':' + minutestring + ampmstring
		strings = (date,time)
		
		return strings
	
class gods_class():
	#this class stores the goods mood about the player
	def __init__(self):
		
		name = save_path + os.sep + 'gods.data'
		
		try:
			
			f = open(name, 'rb')
			screen.render_load(14)
			temp = p.load(f)
			self.mood = temp.mood
			
		except:
			
			screen.render_load(13)
			self.mood = 10
			#the mood of goods is raised by good sacrifices at the altar(see mob.enter()) and sinks if their help is needed or the player give them crap
	
	def judgement(self):
		#this function check the mood of the gods and returns a False if they are unhappy about the player or a True if they are happy
		if self.mood > 0:
			return True
		else:
			return False
class sfX():
	
	def __init__(self):
		
		sfx_path = basic_path + os.sep + 'AUDIO' + os.sep + 'SFX' + os.sep
		
		self.sfx_list = {'walk_dry': pygame.mixer.Sound(sfx_path + 'walk_dry.ogg'),
						'walk_wet': pygame.mixer.Sound(sfx_path + 'walk_wet.ogg'),
						'miss': pygame.mixer.Sound(sfx_path + 'miss.ogg'),
						'hit': pygame.mixer.Sound(sfx_path + 'hit.ogg'),
						'fire': pygame.mixer.Sound(sfx_path + 'fire.ogg'),
						'boom': pygame.mixer.Sound(sfx_path + 'boom.ogg'),
						'chop': pygame.mixer.Sound(sfx_path + 'chop.ogg'),
						'break': pygame.mixer.Sound(sfx_path + 'break.ogg'),
						'lvl_up': pygame.mixer.Sound(sfx_path + 'lvl_up.ogg'),
						'steal' : pygame.mixer.Sound(sfx_path + 'steal.ogg'),
						'loot' : pygame.mixer.Sound(sfx_path + 'loot.ogg'),
						'open' : pygame.mixer.Sound(sfx_path + 'open.ogg'),
						'locked' : pygame.mixer.Sound(sfx_path + 'locked.ogg'),
						'immobilized' : pygame.mixer.Sound(sfx_path + 'immobilized.ogg'),
						'item_break' : pygame.mixer.Sound(sfx_path + 'item_break.ogg'),
						'shatter' : pygame.mixer.Sound(sfx_path + 'shatter.ogg'),
						'got_fish' : pygame.mixer.Sound(sfx_path + 'got_fish.ogg'),
						'no_fish' : pygame.mixer.Sound(sfx_path + 'no_fish.ogg')}
						
	def play(self,sfx_name):
		
		try:
			if pygame.mixer.get_busy():
				sleep(0.1)
				
			if game_options.sfxmode == True:
				self.sfx_list[sfx_name].play()
		except:
			print('SFX error')
				
class bgM():
	
	def  __init__(self):
		
		self.song_played_now = 'No'
		self.last_song = 'No'
		
	def check_for_song(self,play_menu_sound = False,force_play = False):
		
		music_path = basic_path + os.sep + 'AUDIO' + os.sep + 'BGM' + os.sep
		
		try:
			if play_menu_sound == False:
				test = self.song_played_now = world.maplist[player.pos[2]][player.on_map].map_type
		except:
			play_menu_sound = True
		
		if game_options.bgmmode == 1 and play_menu_sound == False:
			if force_play == False:
				self.song_played_now = world.maplist[player.pos[2]][player.on_map].map_type
			else:
				self.last_song = 'FOO'
		else:
			pygame.mixer.music.stop()
		
		if self.song_played_now != self.last_song and play_menu_sound == False and game_options.bgmmode == 1:
			
			try:
				pygame.mixer.music.stop()
			except:
				None
				
			track = music_path + self.song_played_now + '.ogg'
			
			pygame.mixer.music.load(track)
			pygame.mixer.music.play(-1)
		
		elif play_menu_sound == True and game_options.bgmmode == 1:
			
			track = music_path + 'menu.ogg'
			
			pygame.mixer.music.load(track)
			pygame.mixer.music.play(-1)
		
		self.last_song = self.song_played_now


def main():
	
	global screen
	global gra_files
	global tl
	global il
	global ml
	global bgm
	global world
	global gods
	global message
	global player
	global time
	global exitgame
	global playing
	global sfx
	global master_loop
	global game_options
	

	screen = g_screen()
	gra_files = g_files()
	tl = tilelist()
	il = itemlist()
	ml = monsterlist()
	sfx = sfX()
	master_loop = True
	while master_loop:
		bgm = bgM()
		bgm.check_for_song(True)
		master_loop = screen.render_main_menu()	
		if playing == True:
			exitgame = False
			time = time_class()
			world = world_class(tl)
			gods = gods_class()
			message = messager()
			p_attribute = attribute(2,2,2,2,2,10,10)
			p_inventory = inventory()
			player = player_class ('Testificate', 'local_0_0', p_attribute,p_inventory)
			mes = 'Welcome to Roguebox Adventures[' + version +']'
			message.add(mes)
			player.stand_check()
			bgm.check_for_song()
			time.tick()
		
			running = True
	
			while running:
				
				world.maplist[player.pos[2]][player.on_map].time_pass() #make the changes of passing time every new day 
				
				screen.render(0)
				
				if len(message.mes_list) > 3:
					message.clear()
				
				move_border = 0
		
				bodyparts = ('Head', 'Body', 'Legs' , 'Feet')
		
				for i in bodyparts:
			
					if player.inventory.wearing[i] != player.inventory.nothing:
						move_border += 1
				
				move_chance = random.randint(1,9)
				if move_border < move_chance:
					screen.reset_hit_matrix()
					plus = 1
					r = True
					while r:
						test = player.user_input()
						if test == 'next_mes':
							screen.render(0)
						else:
							message.more_messages = False
							r = False
				
				if exitgame == True:
					running = False
					playing = False
				
if __name__ == '__main__':
	
	everything_fine = True
	
	try:
		main()
	except Exception as e:
		import traceback
		everything_fine = False
		exc_type, exc_obj, exc_tb = sys.exc_info()
		bs = save_path
		for c in range(0,6):
			bs = bs.replace('/World'+str(c),'')
		logfile = bs + os.sep + 'debug.txt'
		f = open(logfile,'a')
		f.write('###############################################')
		f.write('\n')
		traceback.print_exception(exc_type, exc_obj, exc_tb, limit=9, file=f)
		f.close()
	finally:
		if everything_fine == False:
			screen.render_crash()
		
