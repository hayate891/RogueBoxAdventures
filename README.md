﻿# RogueBox Adventures

## First things first...

RogueBox Adventures is Free (like in Freedom) Software and distributes under the terms of GPL3 (or later).

This guarantees you the right to:

* share this software,
* use it in any way you like,
* learn from it's code,
* modify it.

To learn more about free software and why it is always a good Idea to use it please visit:

[fsf.org](http://www.fsf.org/)

## What kind of game is RogueBox Adventures?

RBA is a mixture out of Roguelike and Sandbox game. But what does this mean?
    
According to Wikipedia: 

 *"Roguelike is a subgenre of role-playing video games, characterized by procedural generation of game levels, turn-based gameplay, tile-based graphics, permanent death of the player-character, and typically based on a high fantasy narrative setting."*

But RBA doesn't strictly cover all of these points.

* It definitely features procedural generated levels. The whole gameworld is generated randomly for every new game.
* It's gameplay is turn-based but the player has only a limited time to make the next turn (2sec) otherwise the game will go on. Still there is an option to turn a completely turn-based gameplay.
* It uses tile-based graphics (but no ASCII graphics like classic Roguelikes).
* It has an option to play with permanent death (roguelike mode) but it is not required.
* There are monsters like orcs and dryades and items like magic scrolls and weapons inside RBA. So yes, it has got some kind of high fantasy setting.

Sandbox games on the other hand are a special kind of open-world-game which is about the interaction between the player and the game-world. Everything is about changing the gameworld.

RBA is definitely a game about changing the gameworld by interacting with it. So you can call it a sandbox game with some rogue-like elements...
...Or you simply can call it a RogueBox-game.

## What's the story behind the game?
Be patient... it'll come soon :)

## Were can I get the game? On witch platforms does it run?
You can download a build of RBA at: [https://themightyglider.itch.io/roguebox-adventures](https://themightyglider.itch.io/roguebox-adventures)

It is distributed in three ways:

* A Windows-Standalone to run the game on Microsoft Windows PC's
* A Source-Release that should be runnable on any system with a working installation of Python2.7 and pygame. (So the game also runs on OSX, Linux, BSD* and so on) You can download Python at: https://www.python.org/ and pygame at: http://pygame.org. Afterward simply run the file main.py from the main directory of RBA.

## What is about the version numbers?
    
The first number will be changed when the new version isn't compatible with the save files of the old version.

That means a saved game from version 1.0 will be playable on version 1.2 for example but not on version 2.0.

The second number is changed by every release with bugfixes and smaller new features.

In the time between two milestone releases snapshots with version names like 'S170216' will be released in order to illustrate the progress. These snapshots aren't compatible to any other version.

## How do I Play? What are the key-bindings?

RBA can be played with the keyboard, mouse/touchscreen or a gamepad.

The keybindings are:

    w,a,s,d/Arrow-keys/gamepad hat : Move/Navigate trough the menus
    e/ENTER/gamepad Button1        : Interaction/Choose/Use
    i/BACKSPACE/gamepad Button4    : Open Inventory
    b/SPACE/gamepad Button3        : Open Build menu/Switch mode/Done/Drop
    x/ESCAPE/gamepad Button2       : Open main menu/Abrot/Back
    f       /gamepad Button5       : Fire mode on/off

A low-spoiler tutorial on gameplay can be found in tutorial.html file.

## I've found a bug. I want to make a suggestion. I want to contribute something.

You can report bugs on GitHub at: [https://gitgud.io/themightyglider/RogueBoxAdventures](https://gitgud.io/themightyglider/RogueBoxAdventures)

Or you can mail me at: themightyglider@gmx.de (love- or hate-mail is welcome as well)

Contributors please push your changes to the development branch of the git repository.

## Have Fun!

Thank you for being interested in my little game. I hope it will bring you some hours of joy.

	Copyright (C) 2015-2016  Marian Luck
	
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
