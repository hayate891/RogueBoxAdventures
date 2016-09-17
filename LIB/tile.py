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

class tile():
	
	def __init__(self,techID, name, tile_color, use_group, move_group, grow_group, damage, move_message, damage_message, destroy = False, replace = None, civilisation = False, can_grown = False, build_here = True, tile_pos = (0,0), transparency = True, conected_items = None, conected_tiles = None, conected_resources = None, drops_here = True ):
		
		self.techID = techID
		self.name = name
		self.tile_color = tile_color
		self.use_group = use_group
		self.move_group = move_group
		self.grow_group = grow_group
		self.damage = damage
		self.move_mes = move_message
		self.damage_mes = damage_message
		self.destroy = destroy
		self.replace = replace
		self.civilisation = civilisation
		self.can_grown = can_grown
		self.build_here = build_here
		self.tile_pos = tile_pos
		self.transparency = transparency
		self.conected_items = conected_items
		self.conected_tiles = conected_tiles
		self.conected_resources = conected_resources
		self.drops_here = drops_here
