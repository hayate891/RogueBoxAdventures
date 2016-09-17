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

class attribute():

	def __init__(self, p_strange, p_defense, m_strange, m_defense, luck, max_lp, max_mp, hunger_max = 3600, thirst_max = 2160, tiredness_max = 5040, pickaxe_power = 1):
		
		self.p_strange = p_strange
		self.p_defense = p_defense
		self.m_strange = m_strange
		self.m_defense = m_defense
		self.luck = luck
		self.max_lp = max_lp
		self.max_mp = max_mp
		self.hunger = hunger_max
		self.hunger_max = hunger_max
		self.thirst = thirst_max
		self.thirst_max = thirst_max
		self.tiredness = tiredness_max
		self.tiredness_max = tiredness_max
		self.pickaxe_power = pickaxe_power
