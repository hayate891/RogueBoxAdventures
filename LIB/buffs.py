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

#This file contains the definition of the buffs class
#Buffs are effects that work on the player for some rounds. eg.:bleeding
#every player object contains a buff object

class buffs():
	
	def __init__(self):
		
		self.bleeding = 0
		self.hexed = 0
		self.poisoned = 0
		self.immobilized = 0
		self.confused = 0
		self.light = 0
		self.blind = 0
		self.adrenalised = 0
		self.adrenalised_max = 0
		
	def set_buff(self,name,duration):
		
		if name == 'bleeding':
			self.bleeding += duration
		elif name == 'hexed':
			self.hexed += duration
		elif name == 'poisoned':
			self.poisoned += duration
		elif name == 'immobilized':
			self.immobilized += duration
		elif name == 'confused':
			self.confused += duration
		elif name == 'light':
			if duration > self.light:
				self.light = duration#light can't be added on
		elif name == 'blind':
			self.blind += duration
		elif name == 'adrenalised':
			self.adrenalised_max += duration
			if self.adrenalised_max <= 1440:
				self.adrenalised += duration
			else:
				test = duration - (self.adrenalised_max - 1440)
				if test > 0:
					self.adrenalised += test
				
			
			
	def buff_tick(self):
		
		if self.bleeding > 0:
			self.bleeding -= 1
		elif self.bleeding < 0:
			self.bleeding = 0	
		
		if self.hexed > 0:
			self.hexed -= 1
		elif self.hexed < 0:
			self.hexed = 0
			
		if self.poisoned > 0:
			self.poisoned -= 1
		elif self.poisoned < 0:
			self.poisoned = 0
			
		if self.immobilized > 0:
			self.immobilized -= 1
		elif self.immobilized < 0:
			self.immobilized = 0
			
		if self.confused > 0:
			self.confused -= 1
		elif self.confused < 0:
			self.confused = 0
		
		if self.light > 0:
			self.light -= 1
		elif self.light < 0:
			self.light = 0
			
		if self.blind > 0:
			self.blind -= 1
		elif self.blind < 0:
			self.blind = 0
		
		if self.adrenalised > 0:
			self.adrenalised -= 1
		elif self.adrenalised < 0:
			self.adrenalised = 0
			
	def sget(self):
	
		slist = [' ']
		
		if self.bleeding > 0:
			slist.append('BLEEDING(' + str(self.bleeding) + ')')
			
		if self.hexed > 0:
			slist.append('HEXED(' + str(self.hexed) + ')')
			
		if self.poisoned > 0:
			slist.append('POISONED(' + str(self.poisoned) + ')')
			
		if self.immobilized > 0:
			slist.append('IMMOBILIZED(' + str(self.immobilized) + ')')
		
		if self.confused > 0:
			slist.append('CONFUSED(' + str(self.confused) + ')')
			
		if self.light > 0:
			slist.append('LIGHT(' + str(self.light) + ')')
			
		if self.blind > 0:
			slist.append('BLIND(' + str(self.blind) + ')')
			
		if self.adrenalised > 0:
			slist.append('ADRENALISED(' + str(self.adrenalised) + ')')
			
		if len(slist) > 1:
			del slist[0]
			
		if len(slist) > 3:
			new_list = [slist[0],slist[1],slist[2],'more...']
			slist = new_list
		
		return slist
