# Turtlemaze

## Goal Overview

 - We use a webcam, on top of the game, so the game knows everything
 - Tiles, Robot, and Stars may be either video-projected of physical

Note that using an all-virtual setup is equivalent to play on a screen.

## Architecture Overview

A GUI is the center of control for the game, it gets input from the webcam,
and send output to the robot and the video-projector.

On the GUI, we display an "understood" view of the game, a 2D version,
with the robot and stars as they are in reality.

This "understood" view of the game may be enough by itself and may be
playable, if we add a box for virtual cards.

So a typical game goes like:
 - Start the game program
 - Choose a tiling
 - Video project it or build it with physical tiles
 - Place a physical robot, or video project one
 - Robot goes to its starting tile
 - Player place its cards
 - Player click "Run" on the GUI
 - The game goes sequencially:
   - Compute next robot position
   - Make robot go to this position
   - If robot out of grid, end the game
   - If every stars are collected, end the game

Note that the game may never end, a "Reset" button is here to
interrupt the game, and place back the robot to its place, so the
player can change its cards.

The code is split it some standalone, testable, pieces:
 - GUI
 - Grid parser using OpenCV
 - Game engine (Rules, execution of the user program)
 - Robot controller (Trying to keep the robot on its tracks)

The GUI is the central piece making others communicate:
  - Pulls informations from the grid parser
  - Push information to game engine
  - Get instruction back from game engine
  - Push instructions to robot controller
  - Waits from robot controller to tell the robot is at the right place

## Webcam

The webcam gives an overview of the game, by doing three different things:

 - Find the grid and tiles colors
 - Find the robot (By matching a tag placed on it, either pysically
   or by the video-projector)
 - Read the cards (instructions).

The webcam video stream may be split in three different streams:
 - One for the feedback for the GUI
 - One for the grid parser
 - One for the robot controller to spot the robot
