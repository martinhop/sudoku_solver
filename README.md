# Sudoku Game and Solver

# CURRENTLY IN TESTING BUGS MAY EXIST

# Pre-requisites

Python 3.7, 
Pygame 1.9.6, 
suduko_generator.py from https://gist.github.com/lvngd/8c1aafc4851985bbd239bc59153f26f9 (used to generate new random boards in game mode)
 
# Description

This suduko appication to allows the user to play a traditional game of suduko and retrieve the completed grid at the press of a key.  Also allows the user to input known numbers into a empty grid and show a solution to this grid if solvable.

# Menu Screen

- Press 'I' to view instructions
- Press 'S' to enter solver mode.
- Press 'Space' to start new game

# Instruction Screen

- Press 'esc' to return to main menu

# Main Game Screen

Play a traditional game

- Select empty cell with mouse
- Enter value and hit enter to commit
- If number is correct it will be added to the grid
- If number is incorrect a strike will be added
- Game ends when grid is complete or 3 strikes earnt
- Press 'space' at any time to auto complete the grid
- Once complete or game ended press any key to return to main menu

Enter Solver Mode

- Select a known cell and in input number hit enter to commit
- Repeat for all known numbers
- Press 'space' to solve grid
- Once solved press any key to return to main menu


