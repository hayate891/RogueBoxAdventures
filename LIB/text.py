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
 
texts ={'tutorial_1.1' : ('Welcome to the RogueBox Adventures', 
						'Tutorial!',
						'Lesson 1: Moving and interaction',
						'You can move your character by',
						'using [w,a,s,d]',
						'and interact with something by',
						'pressing [e]',
						'while standing on it.'),
		'tutorial_1.2' : ('You will find a guidepost in',
						'the south. Move there and read it!'),
		'info_soon' : ('Test Page',
						'Feature comming soon.'),
		'spear' : ('Spears',
					' ',
					'A spear is a weak melee weapon.'),
		'sword' : ('Swords',
					' ',
					'A sword is a medium melee weapon.'),
		'hammer' : ('Hammers',
					' ',
					'A hammer is a heavy melee weapon.'),
		'rune' : ('Runes',
					' ',
					'A rune is a very weak magical',
					'weapon.'),
		'wand' : ('Wands',
					' ',
					'A wand is a weak magical weapon.'),
		'rune staff' : ('Rune Staffs',
					' ',
					'A rune staff is a medium',
					'magical weapon.'),
		'artefact' : ('Artefacts',
					' ',
					'A artefact is a strong magical',
					'weapon.'),
		'helmet' : ('Helmets',
					' ',
					'A helmet can protect your head',
					'of physical damage.'),
		'armor' : ('Armors',
					' ',
					'A armor can protect your body',
					'of physical damage.'),
		'cuisse' : ('Cuisses',
					' ',
					'A cuisse can protect your legs',
					'of physical damage.'),
		'shoes' : ('Shoes',
					' ',
					'Shoes can protect your feet',
					'of physical damage.'),
		'axe' : ('Axes',
				' ',
				'A axe is a tool to chop',
				'down trees.'),
		'pickaxe'  : ('Pickaxes',
					' ',
					'A pickaxe is a tool to break',
					'rock.'),
		'ring' : ('Rings',
				' ',
				'A ring can increase your will.'),
		'amulet' : ('Amulets',
					' ',
					'A amulet can increase your will.'),
		'talisman' : ('Talismans',
					' ',
					'A talisman can increase your luck.'),
		'necklace' : ('Necklaces',
					' ',
					'A necklace can increase your luck.'),
		'decorative_clothes' : ('Decorative Clothes',
								' ',
								'This item changes the way you',
								'look like.'),
		'Fontain' : ('Fontain',
					' ',
					'Can be placed and used',
					'as water source.'),
		'Chest' : ('Chest',
					' ',
					'Can be placed and used',
					'to store items.'),
		'Bed' : ('Bed',
				' ',
				'Can be placed and used',
				'to sleep inside.'),
		'Carpenter\'s workbench' : ('Carpenter\'s workbench',
									' ',
									'Can be placed and used',
									'to craft wooden furniture.'),
		'Carvers\'s workbench' : ('Carver\'s workbench',
									' ',
									'Can be placed and used',
									'to craft wooden items.'),
		'Stonecutter\'s workbench' : ('Stonecutter\'s workbench',
									' ',
									'Can be placed and used',
									'to craft stone furniture.'),
		'Forger\'s workbench' : ('Forger\'s workbench',
								' ',
								'Can be placed and used',
								'to forge items.'),
		'Alchemist\'s workshop' : ('Alchemist\'s workshop',
									' ',
									'Can be placed and used',
									'to brew potions.'),
		'Furnace' : ('Furnace',
					' ',
					'Can be placed and used',
					'to cook food.'),
		'Altar' : ('Altar',
					' ',
					'Can be placed and used',
					'to worship the gods or',
					'identify items.'),
		'Table' : ('Table',
					' ',
					'Decorative Furniture that',
					'can be placed.'),
		'Wooden seat' : ('Wooden seat',
						' ',
						'Decorative Furniture that',
						'can be placed.'),
		'Stone seat' : ('Stone seat',
						' ',
						'Decorative Furniture that',
						'can be placed.'),
		'Bookshelf' : ('Bookshelf',
						' ',
						'Decorative Furniture that',
						'can be placed.'),
		'Pilar' : ('Pilar',
					' ',
					'Decorative Furniture that',
					'can be placed.'),
		'Fishing rod' : ('Fisching Rod',
						' ',
						'Can be used close to waters',
						'in order to catch fish.'),
		'Blueprint' : ('Blueprint',
						' ',
						'Blueprints change the way your',
						'buildings look like.'),
		'Bomb' : ('Bomb',
				' ',
				'Can be placed and will',
				'explode after 3 turns.'),
		'Scroll' : ('Scroll',
					' ',
					'Scrolls can be used to',
					'cast spells.',
					'They will disappear after',
					'reading them.'),
		'Spellbook' : ('Spellbook',
						' ',
						'Spellbooks can be used to',
						'cast spells.',
						'You will loose your focus',
						'by reading them.'),
		'Mysterious Blue Crystal' : ('Mysterious Blue Crystal',
									' ',
									'Breaking a Mysterious Blue',
									'Crystal will reduce the time',
									'you need to get focused',
									'permanently.'),
		'Heart-Shaped Crystal' : ('Heart-Shaped Crystal',
									' ',
									'Breaking a Heart-Shaped Crystal',
									'will raise your max. LP.'),
		'Enchanted Enhancement Powder' : ('Enchanted Enhancement Powder',
										' ',
										'Enhances worn equipment',
										'randomly.'),
		'Heavy Bag' : ('Heavy Bag',
						' ',
						'What may be inside?'),
		'Torch' : ('Torch',
					' ',
					'Can be used to',
					'illuminate dark places.'),
		'Scrub seed' : ('Scrub seed',
						' ',
						'Can be used to plant',
						'a new scrub.'),
		'Sapling' : ('Sapling',
						' ',
						'Can be used to plant',
						'a new tree.'),
		'Small cactus' : ('Small cactus',
						' ',
						'Can be used to plant',
						'a new cactus.'),
		'Palm sapling' : ('Palm sapling',
						' ',
						'Can be used to plant',
						'a new palm.'),
		'Chalk' : ('Chalk',
					' ',
					'Can be used to write',
					'a magic word on the',
					'ground. Monsters can not',
					'pass this sign.'),
		'Strength' : ('Strenght',
						' ',
						'Increases your ability',
						'to DEAL PHYSICAL DAMAGE.'),
		'Skill' : ('Skill',
						' ',
						'Increases your ability',
						'to AVOID PHYSICAL DAMAGE.'),
		'Power' : ('Power',
						' ',
						'Increases your ability',
						'to DEAL MAGICAL DAMAGE.'),
		'Will' : ('Will',
						' ',
						'Increases your ability',
						'to AVOID MAGICAL DAMAGE.'),
		'Health' : ('Health',
						' ',
						'Increases your number',
						'of HEALTH POINTS.'),
				}
