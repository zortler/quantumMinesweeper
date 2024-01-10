from qiskit import *
import random
import tkinter as tk
from functools import partial
backend = Aer.get_backend('qasm_simulator')


class square(object):
    exploded = False
    clicked = False
    marked = False
    h_marked = False
    circuit = None
    state = 0.0
    h_state = 0.5
    value = 0.0
    h_value = 0.0

# setting up empty
    def __init__(self):
        self.clicked = False
        qc = QuantumCircuit(1)
        measure_bit = ClassicalRegister(1, 'measure_bit')
        qc.add_register(measure_bit)
        self.circuit = qc

    def add1(self):
        self.circuit.x(0)
        self.state = 1.0

    def add_minus(self):
        self.circuit.h(0)
        self.state = 0.5
        self.h_state = 0.0

    def add_plus(self):
        self.circuit.x(0)
        self.circuit.h(0)
        self.state = 0.5
        self.h_state = 1.0

    def measure(self):
        self.circuit.barrier()
        self.circuit.measure(0,0)
        job = backend.run(self.circuit, shots=1)
        result = job.result()
        counts = result.get_counts()
        return list(counts.keys())[0]

    def measure_h(self):
        self.circuit.h(0)
        self.circuit.barrier()
        self.circuit.measure(0,0)
        job = backend.run(self.circuit, shots=1)
        result = job.result()
        counts = result.get_counts()
        return list(counts.keys())[0]


class board(object):

    gameOver = False
    win = False
    buttons = None
    h_buttons = None

    def __init__(self, width, height, num1s, num_plus, num_minus, expert_mode, custom_board = None):

        self.height = height
        self.width = width
        self.num1s = num1s
        self.num_minus = num_minus
        self.num_plus = num_plus
        self.remaining_mines = num1s + num_plus
        self.remaining_squares = width * height - num1s - num_plus
        self.expert_mode = expert_mode

        self.board = [[square() for i in range(width)] for j in range(height)]

        if custom_board is None:
            # setup 1, + and - at random spots

            count = 0
            while count < self.num1s:
                x = random.sample(range(self.height), 1)[0]
                y = random.sample(range(self.width), 1)[0]
                if self.board[x][y].state == 0:
                    self.board[x][y].add1()
                    count += 1

            count = 0
            while count < self.num_plus:
                x = random.sample(range(self.height), 1)[0]
                y = random.sample(range(self.width), 1)[0]
                if self.board[x][y].state == 0:
                    self.board[x][y].add_plus()
                    count += 1

            count = 0
            while count < self.num_minus:
                x = random.sample(range(self.height), 1)[0]
                y = random.sample(range(self.width), 1)[0]
                if self.board[x][y].state == 0:
                    self.board[x][y].add_minus()
                    count += 1

        else:
            # setup custom board

            for x in range(self.height):
                for y in range(self.width):
                    if custom_board[x][y] == "1":
                        self.board[x][y].add1()
                    if custom_board[x][y] == "-":
                        self.board[x][y].add_minus()
                    if custom_board[x][y] == "+":
                        self.board[x][y].add_plus()

    def __str__(self):
        # define print function for our game boards

        returnString = " "
        divider = "\n---"

        for i in range(self.width):
            returnString += " | " + str(i)
            divider += "----"

        returnString += "        "
        divider += "     ---"

        for i in range(self.width):
            returnString += " | " + str(i)
            divider += "----"
        divider += "\n"

        returnString += divider

        for x in range(self.height):
            returnString += str(x) + " |"
            for y in range(self.width):
                if self.board[x][y].exploded:
                    returnString += " X " + "|"
                elif self.board[x][y].marked:
                    returnString += " ■ " + "|"
                elif self.board[x][y].clicked:
                    if self.board[x][y].value == 0:
                        returnString += " # " + "|"
                    else:
                        returnString += str(round(self.board[x][y].value,1)) + "|"
                else:
                    returnString += "   |"

            returnString += "     "
            returnString += str(x) + " |"
            for y in range(self.width):
                if self.board[x][y].exploded:
                    returnString += " X " + "|"
                elif self.board[x][y].h_marked:
                    returnString += " ■ " + "|"
                elif self.board[x][y].clicked:
                    if self.board[x][y].h_value == 0:
                        returnString += " # " + "|"
                    else:
                        returnString += str(round(self.board[x][y].h_value, 1)) + "|"
                else:
                    returnString += "   |"
            returnString += divider
        return returnString

    def setValues(self):

        for x in range(self.height):
            for y in range(self.width):
                sq = self.board[x][y]
                sq.value = 0
                sq.h_value = 0

                for k in range(max(0, x-1), min(self.height, x+2)):
                    for l in range(max(0, y-1), min(self.width, y+2)):
                        if not (k == x and l == y):
                            sq.value += self.board[k][l].state
                            sq.h_value += self.board[k][l].h_state

    def leftClick(self, x, y, h, ver):
        sq = self.board[x][y]
        # if clicked square is already clicked and has value zero, click all remaining adjacent squares
        if sq.clicked:
            if sq.value == 0 or sq.h_value == 0:
                for k in range(max(0, x - 1), min(self.height, x + 2)):
                    for l in range(max(0, y - 1), min(self.width, y + 2)):
                        if not (k == x and l == y):
                            if not self.board[k][l].clicked:
                                if sq.value == 0:
                                    self.leftClick(k,l, False, ver)
                                if sq.h_value == 0:
                                    self.leftClick(k,l,True, ver)
            return
        # if not clicked, measure corresponding qubit and handle the outcome
        sq.clicked = True
        sq.marked = False
        sq.h_marked = False
        if h:
            result = sq.measure_h()
        else:
            result = sq.measure()

        if result == "0":
            self.buttons[x][y]['text'] = sq.value
            self.h_buttons[x][y]['text'] = sq.h_value
            if sq.state + sq.h_state < 1:
                self.remaining_squares -= 1
                if self.remaining_squares == 0:
                    self.win = True
                    if ver == 1:
                        print("\nYou won!")
                        quit()
            else:
                self.remaining_mines -= 1

            # update values for adjacent squares, click all if value is 0
            # if expert_mode is enabled and a neighboring known value updates to 0, click that square
            for k in range(max(0, x-1), min(self.height, x+2)):
                for l in range(max(0, y-1), min(self.width, y+2)):
                    if not (k == x and l == y):
                        self.board[k][l].value -= sq.state
                        self.board[k][l].h_value -= sq.h_state
                        if self.board[k][l].clicked:
                            self.buttons[k][l]['text'] = self.board[k][l].value
                            self.h_buttons[k][l]['text'] = self.board[k][l].h_value
                        if sq.value == 0:
                            self.leftClick(k, l, False, ver)
                        if sq.h_value == 0:
                            self.leftClick(k, l, True, ver)
                        if self.expert_mode == 1 and self.board[k][l].value == 0 and self.board[k][l].clicked:
                            self.leftClick(k, l, False, ver)
                        if self.expert_mode == 1 and self.board[k][l].h_value == 0 and self.board[k][l].clicked:
                            self.leftClick(k, l, True, ver)
        else:
            sq.exploded = True
            self.buttons[x][y]['text'] = "X"
            self.h_buttons[x][y]['text'] = "X"
            self.gameOver = True
            if ver == 1:
                print("\nYou hit a mine, Game Over!")
                quit()

        return True

    def rightClick(self, x, y, h=False):
        sq = self.board[x][y]
        if sq.clicked:
            return False
        if not h:
            if not sq.marked:
                sq.marked = True
            else:
                sq.marked = False
        else:
            if not sq.h_marked:
                sq.h_marked = True
            else:
                sq.h_marked = False
        return True


# Start game
def play(width, height, num1s, num_plus, num_minus, expert_mode, ver, custom_board=None):
    win = False
    brd = board(width, height, num1s, num_plus, num_minus, expert_mode, custom_board)
    brd.setValues()
    window = tk.Tk()
    brd.buttons = [[0 for i in range(width)] for j in range(height)]
    brd.h_buttons = [[0 for i in range(width)] for j in range(height)]
    for x in range(height):
        for y in range(width):
            brd.buttons[x][y] = tk.Button(width=4, height=2, command=partial(brd.leftClick, x, y, False, ver))
            brd.h_buttons[x][y] = tk.Button(width=4, height=2, command=partial(brd.leftClick, x, y, True, ver))
            label = tk.Label(window, width=8, height=2)
            label.grid(row=y, column=width)
            brd.buttons[x][y].grid(row=x, column=y)
            brd.h_buttons[x][y].grid(row=x, column=width + y + 1)
    if ver == 1:
        window.mainloop()
    else:
        while not brd.gameOver:
            print(brd)
            click = int(input("Do you want to Click a square (0) or Mark a Bomb (1)?: "))
            print("Make your move:")
            boardNumber = int(input("On which board do you want to make your move? (0/1): "))
            x = int(input("row: "))
            y = int(input("column: "))
            if click == 0:
                brd.leftClick(x, y, (boardNumber == 1), ver)
            else:
                brd.rightClick(x, y, h=(boardNumber == 1))
            if brd.win and not brd.gameOver:
                brd.gameOver = True
                win = True

        print(brd)
        if win:
            print("You won!")
        else:
            print("You hit a mine, Game Over!")


def main():
    ver = int(input("Do you want to play to console version (0) or the GUI version (1) of the game?: "))
    level = int(input("Which level do you want to play? (levels 1-4, type 0 to set up custom board): "))
    expert_mode = int(input("Do you want to play in expert mode? 1/0 (more info in readme): "))
    if level == 0:
        height = int(input("Choose the Height of the board: "))
        width = int(input("Choose the Width of the board: "))
        num1s = int(input("Choose the Number of 1s on the board: "))
        num_plus = int(input("Choose the Number of +'s on the board: "))
        num_minus = int(input("Choose the Number of -'s on the board: "))
        play(width, height, num1s, num_plus, num_minus, expert_mode, ver)
    elif level == 1:
        height = 4
        width = 4
        num1s = 2
        num_plus = 1
        num_minus = 1
        custom_board = [["0","0","1","-"],
                        ["0","0","0","0"],
                        ["0","0","0","0"],
                        ["1","0","+","0"]]
        play(width, height, num1s, num_plus, num_minus, expert_mode, ver, custom_board=custom_board)

    elif level == 2:
        height = 8
        width = 8
        num1s = 4
        num_plus = 3
        num_minus = 3
        play(width, height, num1s, num_plus, num_minus, expert_mode, ver)

    elif level == 3:
        height = 12
        width = 14
        num1s = 10
        num_plus = 8
        num_minus = 11
        play(width, height, num1s, num_plus, num_minus, expert_mode, ver)

    elif level == 4:
        height = 16
        width = 30
        num1s = 30
        num_plus = 30
        num_minus = 40
        play(width, height, num1s, num_plus, num_minus, expert_mode, ver)


main()
