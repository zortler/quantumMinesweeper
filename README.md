QUANTUM MINESWEEPER 

Raphael Lüscher        
11.01.2024        
Universität Basel

REQUIREMENTS:
  - qiskit
  - qiskit-aer
  - tkinter


EXPLANATION:

I'm sure you're familiar with tha classic game of minesweeper, in which you are given a grid of squares and the goal of the game is to detect all mines (representedby a 1) and click all other remaining squares (represented by a 0). 
If you click on an empty square, it then displays the sum of states of all surrounding squares (I will often call this the squares value), but if you're unlucky enough to hit a mine, you will lose the game. 
Naturally this games is quite binary, since every square is either a useful square or a mine, but we can try to get a bit of variation by adding more than two possible states of squares.

Suppose that every square is hiding a unique qubit behind it, each of which has states in {|0>, |1>, |->, |+>}. If we click a square we will force a measurement on that particular qubit, which will result in:
  - 0 or 1 if the qubit is in state |0> or |1> respectively
  - 50% chance of a 0 and 50% of a 1 if the qubit is in state |-> or |+>
If we measure the qubit to be a 0, the corresponding square of the qubit will now display the sum of the expectation of measurement over all neighboring qubits (So |+> and |-> will both be counted as 1/2).
If we measure the qubit to be a 1, we instantly lose the game.

If we just made these changes without thinking about it too much, we would soon realise that there is no way to distinguish |-> states and |+> states, which would make the game pretty much pointless.
For this reason I added a second playing board to the game, which performs a Hadamard gate on every single qubit on the grid. This essentially just maps |1> states to |+> states, |0> states to |-> states and also vice-verca.
We call the second board "H-Board" and it has all the same properties as the normal board, except that all of it's qubits have had an H-gate applied.
Also note that the H-board acts on the exact same qubits as the normal board, so we can still just measure each square exactly once on both squares. The corresponding state on the other board gets set to |0>.

We consider |0> and |-> states to be "good" in the sense that we can always click them on one of the playing boards and be guaranteed to not lose the game.
On the other hand, you will never be able to click a |1> or |+> states on any board with a nonzero chance of losing. 
Notice however, that you're still going to get away with clicking on squares with |->, |+> states on the normal board 50% of the time. The same is true for |0> and |1> states on the "H-Board".


The game also includes some minor tweaks just to improve user experience a bit, these are:
  - If you click a |0> on the normal board, click all adjacent squares on the normal board.
  - If you click a |-> on the H-board, click all adjacent squares on the H-board.

This was already done in the original Minesweeper game, but this game has a unique property in that square values are allowed to change. If we have a square which only neighbors |0>'s and a single |-> state, 
we will need to update the value of the square on the normal board to 0 once we measure the |-> state on the H-board. These lead to some more minor optimizations:

EXPERT_MODE:

If you decide to enable expert mode, the following additional "rules" will be included:
  - When the value of an already revealed square on the normal board gets updated to a 0, click that square on the normal board.
  - When the value of an already revealed square on the H-board gets updated to a 0, click that square on the H-board.

GUI/CONSOLE VERSION:

You are able to play the game in two different versions. The console version just uses print() commands to print to current state of the game on the console and allows you to either click a square or mark a "bad" square each move.
The GUI version features a simple tkinter interface, which allows you to easily click the squares you want to click on both boards. Sadly this version doesn't have a feature for marking bombs yet, so you might need some additional
visulisation skills to play the GUI version.


LEVEL EXPLANATION:

The game features four different levels of difficulty labeled from 1-4 and also a custom level labeled with 0, where you can choose your own board size and the number of squares with each of the states |1>, |->, |+>.

  LEVEL 1:
  
    The first level can be thought of as a tutorial. It's always the same 4x4 board and there is a strategical way to guarantee a victory when starting with the TOP LEFT square. It contains:
      - 2 |1> STATES
      - 1 |-> STATE
      - 1 |+> STATE

  LEVEL 2:
  
    Played on a 8x8 board with a random distribution of the follwing quantities of states:
      - 4 |1> STATES
      - 3 |-> STATES
      - 3 |+> STATES

  LEVEL 3:
  
    Played on a 12x14 board with a random distribution of the follwing quantities of states:
      - 10 |1> STATES
      - 11 |-> STATES
      - 8 |+> STATES

  LEVEL 4:
  
    Played on a 16x30 board with a random distribution of the follwing quantities of states:
      - 30 |1> STATES
      - 40 |-> STATES
      - 30 |+> STATES


HINTS:

  - The total number of each state in a level as stated just above can be very useful when dealing with only a few remaining squares. Just don't forget to keep track!
  - There will be situations in which you will not be able to make a move without risking some chance of losing the game, but you can still try to find squares where to odds of losing are minimized.



NOTES:

I came up with this concept of a "quantum minesweeper" game as a simple introduction to some core concepts of quantum computing and just a game that could be enjoyed and understood by a large group of people. I tried to
stay true to the simplicity and user friendliness of the original Minesweeper game, while still giving experienced minesweeper players a lot of things to think about.

The layout of the print/__str__ function of the board in the console version of the game is somewhat inspired by https://github.com/RaemondBW/Python-Minesweeper.

While researching after already doing a big part of the project, I noticed that there already existed some other interpretations of a "quantum minesweeper" game. All ideas for additions to this quantum minesweeper game not 
already existing in the original Minesweeper were my own and any similarities are coincidental.
