# Lights-Out
Lights Out game and solver in Python (Pygame)

Using Python and the Pygame package, I've written a simulation of the classic handheld game Lights Out (Tiger Electronics, 1995).

Running the program opens up a game window in which you can choose the size of the game you'd like to play (4x4, 5x5, 6x6, 7x7, or 8x8).
You can then manually toggle certain lights to be on or off at the start of the game, or have the game generate a random solvable board.
If you toggle the lights yourself, the game will verify that the board you've created is solvable before allowing you to begin playing.
Once playing, the game will keep track of the number of button-presses you've used and also work to find a minimal solution.
At any time, you can press a "Solve" button to have the computer solve the puzzle (i.e. turn out all the lights) algorithmically.
The game also learns better solving techniques over time (which are saved in the file KS.p)
