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

class countdown():
	
	def __init__(self, kind, x, y, countfrom, data='None'):
	# countdown objects are used to initialize a event after a  certain number of turns. They are bound to a certain map.
	#kind: is a string and tell the min programm what kind of event should be done
	#x,y: cordinates of the tile that is affected by the event
	#countfrom: number of turns
	#data: some specific variable that is needed for this special kind of countdown
	
		self.kind = kind
		self.x = x
		self.y = y
		self.count = countfrom
		self.data = data
	
	def countdown(self):
	#count down and check if it got 0
		if self.count > 0:
			self.count -= 1
		
		if self.count < 0:
			print('count to low')
			self.count = 1
		
		print(self.kind,self.count)
		
		if self.count <= 0:
			return True
		else:
			return False 
