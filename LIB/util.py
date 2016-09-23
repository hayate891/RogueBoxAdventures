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

import pickle as p
from version import release_number
import os

try:
	from urllib import urlopen
except:
	from urllib.request import urlopen as urlopen

def save(world,player,time,gods,path,sep):
	#this function is called if the game is closed
	#it needs the world object, the player object, the time object, the basic_path and os.sep from the main programm
	
	name1 = path + sep + 'world.data'
	
	f = open(name1, 'wb')
	p.dump(world,f,0)
	f.close()
	
	name2 = path + sep + 'player.data'
	
	f = open(name2, 'wb')
	p.dump(player,f,0)
	f.close()
	
	name3 = path + sep + 'time.data'
	
	f = open(name3, 'wb')
	p.dump(time,f,0)
	f.close()
	
	name4 = path + sep + 'gods.data'
	
	f = open(name4, 'wb')
	p.dump(gods,f,0)
	f.close()

def save_options(options,path,sep):
	
	name2 = path + sep + 'options.data'
	
	f = open(name2, 'wb')
	p.dump(options,f,0)
	f.close()

class game_options():
	
	def __init__(self,basic_path,home_save):
		
		if home_save == False:
			name = basic_path + os.sep + 'SAVE' + os.sep + 'options.data'
		else:
			name = os.path.expanduser('~') + os.sep + '.config' + os.sep + 'RogueBox-Adventures' + os.sep + 'SAVE' + os.sep + 'options.data'
		
		try:
			f = open(name, 'rb')
			temp = p.load(f)
			self.screenmode = temp.screenmode
			self.bgmmode = temp.bgmmode
			self.sfxmode = temp.sfxmode
			self.turnmode = temp.turnmode
			self.mousepad = temp.mousepad
			self.check_version = temp.check_version
		
		except:
			self.screenmode = 1 #0:windowed,1:fullscreen
			self.bgmmode = 1 #0:bgm off, 1:bgm on
			self.sfxmode = 1 #0:sfx off, 1:sfx on
			self.turnmode = 1 #0:classic, 1:Semi-Real-Time
			self.mousepad = 0 #0:mouse off, 1:mouse on
			self.check_version = 0 #0:check off 1:check on
			replace_string = os.sep + 'options.data'
			save_path = name.replace(replace_string,'')
			save_options(self,save_path,os.sep)


def check_version():
	#this function compares the release_number from version.py whit a number that from the https://notabug.org/themightyglider/themightyglider.notabug.org/raw/master/index.html
	#and returns: 'This version is up to date', 'Old version!!! Please update.', 'Can't reach server!'
	try:
		f = urlopen('https://notabug.org/themightyglider/rba-version/raw/master/version.htm')
		vers_test = int(f.read())
		
		if release_number ==  vers_test:
			return 'This version is up to date.'
		else:
			return 'Old version!!! Please update.'
	except:
			return 'Can\'t reach server!'
